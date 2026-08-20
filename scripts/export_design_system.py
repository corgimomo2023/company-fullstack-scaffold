"""Generate implementation artifacts from the repository's normative DESIGN.md.

The upstream @google/design.md 0.4.0 exporter omits line-height from all three
formats and emits DTCG letter-spacing values in unsupported `em` units. This
wrapper preserves the complete source contract, adds plain CSS and Tailwind
preset consumers, and carries component behavior through namespaced DTCG data.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CLI_PACKAGE = "@google/design.md@0.4.0"
OUTPUTS = {
    "theme.css": "css-tailwind",
    "tailwind.theme.json": "json-tailwind",
    "tokens.json": "dtcg",
}
EXTENSION_KEY = "com.github.corgimomo2023.company-fullstack-scaffold"
DISPLAY_STACK = [
    "Pragati Narrow",
    "Noto Sans TC",
    "Microsoft JhengHei",
    "Arial Narrow",
    "sans-serif",
]
BODY_STACK = ["Roboto", "Noto Sans TC", "Microsoft JhengHei", "Arial", "sans-serif"]


def typography_stack(spec: dict[str, Any]) -> list[str]:
    return DISPLAY_STACK if spec["fontFamily"] == "Pragati Narrow" else BODY_STACK


def css_font_stack(spec: dict[str, Any]) -> str:
    return ", ".join(
        item if item == "sans-serif" else json.dumps(item)
        for item in typography_stack(spec)
    )


def build_component_implementation(
    components: dict[str, Any], behavior: dict[str, Any]
) -> dict[str, Any]:
    """Resolve known visual states and label every remaining state behavior-only."""
    explicit = {
        ("button", "primary", "default"): "button-primary",
        ("button", "primary", "hover"): "button-primary-hover",
        ("button", "primary", "active"): "button-primary-active",
        ("button", "primary", "disabled"): "button-primary-disabled",
        ("button", "secondary", "default"): "button-secondary",
        ("button", "secondary", "hover"): "button-secondary-hover",
        ("button", "secondary", "disabled"): "button-secondary-disabled",
        ("button", "accent", "default"): "button-accent",
        ("tag-filter", "default", "default"): "tag-default",
        ("tag-filter", "default", "hover"): "tag-default",
        ("tag-filter", "selected", "default"): "tag-selected",
        ("tag-filter", "selected", "active"): "tag-selected",
        ("card", "default", "default"): "card-default",
        ("card", "selected", "default"): "card-selected",
        ("card", "selected", "selected"): "card-selected",
    }
    status_refs = {
        "neutral": "status-neutral",
        "success": "status-success",
        "warning": "status-warning",
        "danger": "status-danger",
        "information": "status-neutral",
    }
    implementation: dict[str, Any] = {}
    for family, contract in behavior.items():
        mappings: dict[str, Any] = {}
        mapped_count = 0
        for variant in contract["variants"]:
            for state in contract["states"]:
                style_ref = explicit.get((family, variant, state))
                if family in {"text-input", "textarea", "select"}:
                    if state == "focus-visible":
                        style_ref = "input-focus"
                    elif state == "disabled":
                        style_ref = "input-disabled"
                    elif state in {
                        "default",
                        "empty",
                        "populated",
                        "hover",
                        "readonly",
                    }:
                        style_ref = "input-default"
                elif family == "status-badge":
                    style_ref = status_refs[variant]
                elif family == "navigation" and state == "current":
                    style_ref = "navigation-active"

                key = f"{variant}.{state}"
                if style_ref:
                    if style_ref not in components:
                        raise KeyError(
                            f"Missing visual style {style_ref!r} for {family}.{key}"
                        )
                    mappings[key] = {"status": "mapped", "styleRef": style_ref}
                    mapped_count += 1
                else:
                    mappings[key] = {
                        "status": "behavior-only",
                        "note": "Consumer must implement and verify this state; no resolved visual record is claimed.",
                    }
        implementation[family] = {
            "coverage": "complete" if mapped_count == len(mappings) else "partial",
            "mappedCount": mapped_count,
            "behaviorOnlyCount": len(mappings) - mapped_count,
            "stateMappings": mappings,
        }
    return implementation


def load_design(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path} has no YAML front matter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise TypeError("DESIGN.md front matter must be a mapping")
    return data


def exporter_groups(design: dict[str, Any]) -> dict[str, dict[str, Any]]:
    groups = {
        item["name"]: item["values"] for item in design["x-exporter-config"]["groups"]
    }
    required = {"breakpoints", "containers", "elevation", "motion"}
    if set(groups) != required:
        raise ValueError(f"x-exporter-config groups must be {sorted(required)}")
    return groups


def run_export(design_path: Path, export_format: str) -> str:
    result = subprocess.run(
        [
            "npx",
            "-y",
            CLI_PACKAGE,
            "export",
            "--format",
            export_format,
            str(design_path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_css_size_rem(value: Any) -> float:
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)rem", str(value).strip())
    if not match:
        raise ValueError(f"Expected rem font size, got {value!r}")
    return float(match.group(1))


def dtcg_letter_spacing(letter_spacing: Any, font_size: Any) -> dict[str, Any]:
    value = str(letter_spacing).strip()
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)(em|rem|px)", value)
    if not match:
        raise ValueError(f"Unsupported letterSpacing {letter_spacing!r}")
    amount = float(match.group(1))
    unit = match.group(2)
    if unit == "em":
        amount *= parse_css_size_rem(font_size)
        unit = "rem"
    return {"value": round(amount, 6), "unit": unit}


def enrich_css(base: str, design: dict[str, Any]) -> str:
    lines = base.rstrip().splitlines()
    closing = lines.pop()
    if closing.strip() != "}":
        raise ValueError("Unexpected css-tailwind export shape")
    lines.append("  /* Composite and extended tokens retained by export wrapper. */")
    company = exporter_groups(design)
    for name, spec in design["typography"].items():
        font_prefix = f"  --font-{name}:"
        font_index = next(
            index for index, line in enumerate(lines) if line.startswith(font_prefix)
        )
        lines[font_index] = f"{font_prefix} {css_font_stack(spec)};"
        lines.append(f"  --leading-{name}: {spec['lineHeight']};")
    for name, value in company["breakpoints"].items():
        lines.append(f"  --breakpoint-{name}: {value};")
    for name, value in company["containers"].items():
        lines.append(f"  --container-{name}: {value};")
    for name, value in company["elevation"].items():
        lines.append(f"  --shadow-{name}: {value};")
    for name, value in company["motion"].items():
        prefix = "--ease" if name.startswith("easing-") else "--duration"
        suffix = name.removeprefix("easing-")
        lines.append(f"  {prefix}-{suffix}: {value};")
    lines.append(closing)
    return "\n".join(lines) + "\n"


def enrich_tailwind_data(base: str, design: dict[str, Any]) -> dict[str, Any]:
    data = json.loads(base)
    extend = data["theme"]["extend"]
    company = exporter_groups(design)
    font_sizes = extend["fontSize"]
    for name, spec in design["typography"].items():
        font_sizes[name][1]["lineHeight"] = str(spec["lineHeight"])
        extend["fontFamily"][name] = typography_stack(spec)
    extend["screens"] = company["breakpoints"]
    extend["maxWidth"] = {
        f"container-{name}": value for name, value in company["containers"].items()
    }
    extend["boxShadow"] = company["elevation"]
    extend["transitionDuration"] = {
        name: value
        for name, value in company["motion"].items()
        if not name.startswith("easing-")
    }
    extend["transitionTimingFunction"] = {
        name.removeprefix("easing-"): value
        for name, value in company["motion"].items()
        if name.startswith("easing-")
    }
    return data


def enrich_tailwind(base: str, design: dict[str, Any]) -> str:
    return (
        json.dumps(enrich_tailwind_data(base, design), ensure_ascii=False, indent=2)
        + "\n"
    )


def foundation_css(design: dict[str, Any]) -> str:
    lines = [":root {"]
    for name, value in design["colors"].items():
        lines.append(f"  --color-{name}: {str(value).lower()};")
    lines.extend(
        [
            '  --font-display: "Pragati Narrow", "Noto Sans TC", "Microsoft JhengHei", "Arial Narrow", sans-serif;',
            '  --font-body: "Roboto", "Noto Sans TC", "Microsoft JhengHei", Arial, sans-serif;',
        ]
    )
    for name, spec in design["typography"].items():
        family = (
            "var(--font-display)"
            if spec["fontFamily"] == "Pragati Narrow"
            else "var(--font-body)"
        )
        lines.extend(
            [
                f"  --font-{name}: {family};",
                f"  --text-{name}: {spec['fontSize']};",
                f"  --weight-{name}: {spec['fontWeight']};",
                f"  --leading-{name}: {spec['lineHeight']};",
                f"  --tracking-{name}: {spec['letterSpacing']};",
            ]
        )
    for name, value in design["rounded"].items():
        lines.append(f"  --radius-{name}: {value};")
    for name, value in design["spacing"].items():
        lines.append(f"  --spacing-{name}: {value};")
    company = exporter_groups(design)
    for group, prefix in (
        ("breakpoints", "breakpoint"),
        ("containers", "container"),
        ("elevation", "shadow"),
    ):
        for name, value in company[group].items():
            lines.append(f"  --{prefix}-{name}: {value};")
    for name, value in company["motion"].items():
        prefix = "ease" if name.startswith("easing-") else "duration"
        lines.append(f"  --{prefix}-{name.removeprefix('easing-')}: {value};")
    lines.append("}")
    for name in design["typography"]:
        lines.extend(
            [
                "",
                f".type-{name} {{",
                f"  font-family: var(--font-{name});",
                f"  font-size: var(--text-{name});",
                f"  font-weight: var(--weight-{name});",
                f"  line-height: var(--leading-{name});",
                f"  letter-spacing: var(--tracking-{name});",
                "}",
            ]
        )
    return "\n".join(lines) + "\n"


def enrich_dtcg(
    base: str, design: dict[str, Any], design_path: Path
) -> tuple[str, str]:
    data = json.loads(base)
    typography = design["typography"]
    for name, spec in typography.items():
        value = data["typography"][name]["$value"]
        value["lineHeight"] = spec["lineHeight"]
        value["letterSpacing"] = dtcg_letter_spacing(
            spec["letterSpacing"], spec["fontSize"]
        )

    components = design["components"]
    behavior = design["x-component-behavior"]
    company = exporter_groups(design)
    implementation = build_component_implementation(components, behavior)
    visual_evidence: dict[str, Any] = {}
    for name, evidence in design["x-visual-component-evidence"].items():
        record = dict(evidence)
        source_behavior = record.get("sourceBehavior")
        if source_behavior:
            record.update(behavior[source_behavior]["evidence"])
            record["sourceBehavior"] = source_behavior
        visual_evidence[name] = record
    data["$extensions"] = {
        EXTENSION_KEY: {
            "generator": f"{CLI_PACKAGE} plus scripts/export_design_system.py",
            "normativeSource": str(design_path.relative_to(ROOT)),
            "componentContract": components,
            "componentBehavior": behavior,
            "componentImplementation": implementation,
            "visualComponentEvidence": visual_evidence,
            "breakpoints": company["breakpoints"],
            "containers": company["containers"],
            "elevation": company["elevation"],
            "motion": company["motion"],
        }
    }
    component_output = {
        "schema_version": 2,
        "normative_source": str(design_path.relative_to(ROOT)),
        "reference_syntax": "DESIGN.md curly-brace token reference",
        "components": components,
        "behavior_contracts": behavior,
        "implementation_coverage": implementation,
        "visual_component_evidence": visual_evidence,
    }
    return (
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        json.dumps(component_output, ensure_ascii=False, indent=2) + "\n",
    )


def build(design_path: Path) -> dict[str, str]:
    design = load_design(design_path)
    raw = {
        filename: run_export(design_path, export_format)
        for filename, export_format in OUTPUTS.items()
    }
    tailwind_data = enrich_tailwind_data(raw["tailwind.theme.json"], design)
    tailwind_json = json.dumps(tailwind_data, ensure_ascii=False, indent=2) + "\n"
    dtcg, components = enrich_dtcg(raw["tokens.json"], design, design_path)
    return {
        "theme.css": enrich_css(raw["theme.css"], design),
        "foundation.css": foundation_css(design),
        "tailwind.theme.json": tailwind_json,
        "tailwind.preset.cjs": (
            "// Generated from DESIGN.md. Do not edit.\nmodule.exports = "
            + json.dumps(tailwind_data, ensure_ascii=False, indent=2)
            + "\n"
        ),
        "tokens.json": dtcg,
        "components.json": components,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, default=ROOT / "DESIGN.md")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "design-system")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    outputs = build(args.design.resolve())
    drift: list[str] = []
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in outputs.items():
        path = args.output_dir / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                drift.append(filename)
        else:
            path.write_text(content, encoding="utf-8")

    if drift:
        print("Generated design-system artifacts are stale: " + ", ".join(drift))
        return 1
    print(
        ("Verified" if args.check else "Generated")
        + f" {len(outputs)} design-system artifacts"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
