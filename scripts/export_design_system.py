"""Generate implementation artifacts from the repository's normative DESIGN.md.

The upstream @google/design.md 0.4.0 exporter omits line-height from all three
formats and emits DTCG letter-spacing values in unsupported `em` units. This
wrapper preserves the source contract and adds the component definitions as a
namespaced DTCG extension plus a framework-neutral JSON artifact.
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


def load_design(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path} has no YAML front matter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise TypeError("DESIGN.md front matter must be a mapping")
    return data


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


def enrich_css(base: str, typography: dict[str, Any]) -> str:
    lines = base.rstrip().splitlines()
    closing = lines.pop()
    if closing.strip() != "}":
        raise ValueError("Unexpected css-tailwind export shape")
    lines.append(
        "  /* Composite typography line heights retained by export wrapper. */"
    )
    for name, spec in typography.items():
        lines.append(f"  --leading-{name}: {spec['lineHeight']};")
    lines.append(closing)
    return "\n".join(lines) + "\n"


def enrich_tailwind(base: str, typography: dict[str, Any]) -> str:
    data = json.loads(base)
    font_sizes = data["theme"]["extend"]["fontSize"]
    for name, spec in typography.items():
        font_sizes[name][1]["lineHeight"] = str(spec["lineHeight"])
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


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
    data["$extensions"] = {
        EXTENSION_KEY: {
            "generator": f"{CLI_PACKAGE} plus scripts/export_design_system.py",
            "normativeSource": str(design_path.relative_to(ROOT)),
            "componentContract": components,
        }
    }
    component_output = {
        "schema_version": 1,
        "normative_source": str(design_path.relative_to(ROOT)),
        "reference_syntax": "DESIGN.md curly-brace token reference",
        "components": components,
    }
    return (
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        json.dumps(component_output, ensure_ascii=False, indent=2) + "\n",
    )


def build(design_path: Path) -> dict[str, str]:
    design = load_design(design_path)
    typography = design["typography"]
    raw = {
        filename: run_export(design_path, export_format)
        for filename, export_format in OUTPUTS.items()
    }
    dtcg, components = enrich_dtcg(raw["tokens.json"], design, design_path)
    return {
        "theme.css": enrich_css(raw["theme.css"], typography),
        "tailwind.theme.json": enrich_tailwind(raw["tailwind.theme.json"], typography),
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
