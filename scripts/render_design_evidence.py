"""Render a human-readable token/component evidence register.

Inputs are deterministic audit/config artifacts. The output provides clickable
live URLs and page locations only where directly observed; normalized entries
are explicitly marked as not observed rather than borrowing generic pages.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "design-system" / "evidence"
DEFAULT_OUTPUT = ROOT / "docs" / "design-system" / "source-evidence.md"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cell(value: Any) -> str:
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", " ")


def page_links(locations: list[dict[str, Any]], limit: int = 3) -> str:
    if not locations:
        return "Not observed in rendered DOM; see CSS evidence/classification"
    links = []
    for item in locations[:limit]:
        url = item["url"]
        location = item.get("page_location") or "page"
        links.append(f"[{location}]({url})")
    return "<br>".join(links)


def scope_values(values: list[str]) -> str:
    return "<br>".join(f"`{cell(item)}`" for item in values) or "`not observed`"


def css_sources(record: dict[str, Any]) -> str:
    sources = record.get("source_stylesheets", [])
    return "<br>".join(f"[CSS {index + 1}]({url})" for index, url in enumerate(sources))


def token_selector_excerpt(record: dict[str, Any]) -> str:
    declarations = record.get("css_declarations", [])
    excerpts = []
    for declaration in declarations[:2]:
        selectors = declaration.get("selectors", [])
        if selectors and isinstance(selectors[0], dict):
            selector = selectors[0].get("selector", "")
        else:
            selector = selectors[0] if selectors else ""
        prop = declaration.get("property") or next(
            iter(declaration.get("properties", {})), ""
        )
        if selector:
            excerpts.append(f"`{selector}` / `{prop}`")
    media = record.get("media_queries", [])
    if media:
        excerpts.append(f"`@media ({media[0]['media_query']})`")
    return "<br>".join(excerpts) or "Normalized token; no exact declaration match"


def public_component_css(record: dict[str, Any]) -> str:
    excerpts = []
    for stylesheet in record.get("css_selector_evidence", []):
        url = stylesheet["source_url"]
        selectors = stylesheet.get("selectors", [])
        label = selectors[0] if selectors else "selector inventory"
        excerpts.append(f"[`{cell(label)}`]({url})")
    return "<br>".join(excerpts) or "No positive CSS selector match"


def public_component_states(record: dict[str, Any]) -> str:
    states = record.get("state_evidence", {})
    if not states:
        return "`not observed`"
    return "<br>".join(f"`{cell(state)}`" for state in states)


def visual_state(name: str) -> str:
    for state in (
        "hover",
        "active",
        "disabled",
        "focus",
        "selected",
        "success",
        "danger",
        "warning",
        "neutral",
    ):
        if name.endswith(f"-{state}"):
            return state
    return "default"


def visual_live_state(
    source: dict[str, Any], evidence: dict[str, Any], state: str
) -> str:
    if evidence["classification"] in {
        "normalized-product",
        "accessibility-correction",
    }:
        return "`source pattern observed; normalized variant not observed live`"
    source_records = [
        source["public_component_evidence"].get(component, {})
        for component in evidence["sourceComponents"]
    ]
    if state == "default" and any(
        record.get("live_page_locations") for record in source_records
    ):
        return "`public DOM pattern observed; exact scaffold variant not established`"
    if any(state in record.get("state_evidence", {}) for record in source_records):
        return "`source CSS state selector observed`"
    return "`not observed as live state`"


def build_markdown() -> str:
    source = load_json(EVIDENCE_DIR / "source-evidence-index.json")
    computed = load_json(EVIDENCE_DIR / "computed-style-walkthrough.json")
    components = load_json(ROOT / "design-system" / "components.json")
    successful_state_samples = sum(
        len(result.get("states", {})) for result in computed["results"]
    )

    lines = [
        "# Asia Allied source evidence register",
        "",
        f"Audit date: `{source['audit_date']}`.",
        "",
        "> This is a factual research index, not an official Asia Allied design-system publication. `observed-*` means directly found in the public CSS/DOM. `normalized-*`, `normalized-product`, and `accessibility-correction` mean the scaffold deliberately adapted an observed pattern.",
        "",
        "## Coverage",
        "",
        "- Exhaustive sitemap inventory: [site-map-and-template-audit.json](evidence/site-map-and-template-audit.json)",
        "- Raw CSS declarations/selectors: [css-token-evidence.json](evidence/css-token-evidence.json)",
        "- Machine-readable evidence map: [source-evidence-index.json](evidence/source-evidence-index.json)",
        "- Responsive computed styles: [computed-style-walkthrough.json](evidence/computed-style-walkthrough.json)",
        f"- Token evidence records: `{len(source['token_evidence'])}`",
        f"- Public component families: `{len(source['public_component_evidence'])}`",
        f"- Rendered profile/viewport records: `{computed['resultCount']}` (`{len(computed['profiles'])}` route/content profiles × `{len(computed['viewports'])}` viewports)",
        f"- Successful visible state samples: `{successful_state_samples}`",
        "",
        "## Foundation tokens",
        "",
        "| Token | Normative value | Classification | Live page + location | Source CSS | Selector/declaration evidence | Viewports | State | Evidence method |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for name, record in source["token_evidence"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{cell(name)}`",
                    f"`{cell(record['value'])}`",
                    f"`{cell(record['classification'])}`",
                    page_links(record["live_page_locations"]),
                    css_sources(record),
                    token_selector_excerpt(record),
                    scope_values(record["viewport_scope"]),
                    scope_values(record["state_scope"]),
                    "<br>".join(
                        f"`{cell(item)}`" for item in record["evidence_methods"]
                    ),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Public-site component families",
            "",
            "| Component | Classification | DOM/CSS markers | Live page + template location | Source selector | Observed states | Viewports | Evidence method |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for name, record in source["public_component_evidence"].items():
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{cell(name)}`",
                    f"`{cell(record['classification'])}`",
                    "<br>".join(f"`{cell(marker)}`" for marker in record["markers"]),
                    page_links(record["live_page_locations"]),
                    public_component_css(record),
                    public_component_states(record),
                    scope_values(record["viewport_scope"]),
                    "<br>".join(
                        f"`{cell(item)}`" for item in record["evidence_methods"]
                    ),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Product component behavior contracts",
            "",
            "| Contract | Classification | Variants / states | Implementation coverage | Public source pattern | Live page + location |",
            "|---|---|---|---|---|---|",
        ]
    )
    for name, contract in components["behavior_contracts"].items():
        evidence = contract["evidence"]
        implementation = components["implementation_coverage"][name]
        links = "<br>".join(
            f"[{cell(location)}]({url})"
            for url, location in zip(
                evidence["sourceUrls"], evidence["pageLocations"], strict=True
            )
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{cell(name)}`",
                    f"`{cell(evidence['classification'])}`",
                    f"variants `{cell(contract['variants'])}`<br>states `{cell(contract['states'])}`",
                    f"mapped `{implementation['mappedCount']}`<br>behavior-only `{implementation['behaviorOnlyCount']}`",
                    "<br>".join(
                        f"`{cell(component)}`"
                        for component in evidence["sourceComponents"]
                    ),
                    links,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Visual component variants",
            "",
            "> These are scaffold visual mappings, not a claim that every exact state appeared in rendered public DOM. Source links prove the originating pattern; the live-state column distinguishes rendered defaults, CSS-only state selectors and states not observed live.",
            "",
            "| Variant | Classification | Product state | Live-state evidence | Public source pattern | Live page + location | Viewport scope | Evidence method |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for name, evidence in components["visual_component_evidence"].items():
        state = visual_state(name)
        links = "<br>".join(
            f"[{cell(location)}]({url})"
            for url, location in zip(
                evidence["sourceUrls"], evidence["pageLocations"], strict=True
            )
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{cell(name)}`",
                    f"`{cell(evidence['classification'])}`",
                    f"`{state}`",
                    visual_live_state(source, evidence, state),
                    "<br>".join(
                        f"`{cell(component)}`"
                        for component in evidence["sourceComponents"]
                    ),
                    links,
                    "`desktop`<br>`tablet`<br>`mobile`",
                    "`DESIGN.md normalized mapping + linked public pattern`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Responsive rendered profiles",
            "",
            "| Functional/content profile | Live URL | Viewports checked |",
            "|---|---|---|",
        ]
    )
    viewport_names = ", ".join(item["name"] for item in computed["viewports"])
    for profile in computed["profiles"]:
        lines.append(
            f"| `{cell(profile['name'])}` | [{cell(profile['url'])}]({profile['url']}) | `{viewport_names}` |"
        )

    lines.extend(
        [
            "",
            "## Cross-check rule",
            "",
            "When changing a token or component, open at least one linked live page, inspect the listed page location, compare the source selector/declaration where applicable, and then verify the desktop/tablet/mobile record. If the source no longer matches, rerun the audit before changing `DESIGN.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = build_markdown()
    if args.check:
        if (
            not args.output.exists()
            or args.output.read_text(encoding="utf-8") != content
        ):
            print(f"Evidence register is stale: {args.output}")
            return 1
        print(f"Verified evidence register: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Rendered evidence register: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
