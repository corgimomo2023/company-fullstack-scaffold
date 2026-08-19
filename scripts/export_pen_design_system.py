from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOKENS_PATH = ROOT / "design-system" / "tokens.json"
COMPONENTS_PATH = ROOT / "design-system" / "components.json"
OUTPUT_PATH = ROOT / "design-system" / "asia-allied-design-system.pen"

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1240
GUTTER = 40


def text(
    node_id: str,
    content: str,
    *,
    size: int = 16,
    weight: int = 400,
    color: str = "$color-text",
    family: str = "Roboto",
    width: int | str = "fill_container",
    line_height: float = 1.35,
) -> dict[str, Any]:
    return {
        "type": "text",
        "id": node_id,
        "content": content,
        "width": width,
        "height": "fit_content",
        "textGrowth": "fixed-width",
        "fontFamily": family,
        "fontSize": size,
        "fontWeight": str(weight),
        "lineHeight": line_height,
        "fill": color,
    }


def frame(
    node_id: str,
    name: str,
    children: list[dict[str, Any]],
    *,
    layout: str = "vertical",
    gap: int = 16,
    padding: int | list[int] = 24,
    width: int | str = "fill_container",
    height: int | str = "fit_content",
    fill: str = "$color-surface",
    corner_radius: int | str = "$radius-md",
    **extra: Any,
) -> dict[str, Any]:
    value: dict[str, Any] = {
        "type": "frame",
        "id": node_id,
        "name": name,
        "layout": layout,
        "gap": gap,
        "padding": padding,
        "width": width,
        "height": height,
        "fill": fill,
        "cornerRadius": corner_radius,
        "children": children,
    }
    value.update(extra)
    return value


def section(
    node_id: str,
    name: str,
    subtitle: str,
    body: list[dict[str, Any]],
    *,
    column: int,
    row: int,
    fill: str = "$color-surface",
) -> dict[str, Any]:
    return frame(
        node_id,
        name,
        [
            text(
                f"{node_id}-title", name, size=34, weight=700, family="Pragati Narrow"
            ),
            text(f"{node_id}-subtitle", subtitle, size=14, color="$color-text-muted"),
            *body,
        ],
        gap=20,
        padding=40,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        fill=fill,
        clip=True,
        x=column * (CANVAS_WIDTH + GUTTER),
        y=row * (CANVAS_HEIGHT + GUTTER),
        effect={
            "type": "shadow",
            "shadowType": "outer",
            "offset": {"x": 0, "y": 8},
            "blur": 24,
            "spread": 0,
            "color": "#001c191a",
        },
    )


def token_hex(tokens: dict[str, Any], name: str) -> str:
    return tokens["color"][name]["$value"]["hex"]


def token_px(tokens: dict[str, Any], group: str, name: str) -> int:
    return int(tokens[group][name]["$value"]["value"])


def build_document(
    tokens: dict[str, Any], components: dict[str, Any]
) -> dict[str, Any]:
    color_names = [
        "primary",
        "primary-dark",
        "primary-active",
        "accent",
        "accent-accessible",
        "accent-selected",
        "text-on-accent",
        "text",
        "text-muted",
        "surface",
        "surface-subtle",
        "surface-muted",
        "surface-disabled",
        "border",
        "table-header",
        "focus",
        "danger",
        "success",
        "logo-orange",
        "logo-olive",
    ]
    variables: dict[str, Any] = {
        f"color-{name}": {"type": "color", "value": token_hex(tokens, name)}
        for name in color_names
    }
    variables.update(
        {
            f"spacing-{name}": {
                "type": "number",
                "value": token_px(tokens, "spacing", name),
            }
            for name in (
                "2xs",
                "xs",
                "sm",
                "md",
                "lg",
                "xl",
                "2xl",
                "3xl",
                "4xl",
                "5xl",
            )
        }
    )
    variables.update(
        {
            f"radius-{name}": {
                "type": "number",
                "value": token_px(tokens, "rounded", name),
            }
            for name in ("none", "sm", "md", "pill")
        }
    )

    cover = section(
        "cover",
        "Cover",
        "Visual derivative of DESIGN.md · generated, not a second source of truth",
        [
            frame(
                "cover-brand-band",
                "Brand band",
                [
                    text(
                        "cover-kicker",
                        "ASIA ALLIED-INSPIRED PRODUCT FOUNDATION",
                        size=14,
                        weight=700,
                        color="$color-accent",
                    ),
                    text(
                        "cover-heading",
                        "Company Design System",
                        size=68,
                        weight=700,
                        color="$color-surface",
                        family="Pragati Narrow",
                    ),
                    text(
                        "cover-copy",
                        "Evidence-based digital baseline for admin, CMS and operational products.",
                        size=22,
                        color="$color-surface",
                        line_height=1.45,
                    ),
                ],
                gap=24,
                padding=48,
                height=430,
                fill="$color-primary-dark",
                corner_radius="$radius-none",
            ),
            frame(
                "cover-facts",
                "Coverage facts",
                [
                    text(
                        "cover-fact-a",
                        "10,666 unique sitemap URLs",
                        size=22,
                        weight=700,
                    ),
                    text(
                        "cover-fact-b",
                        "559 locale-specific route signatures · 559/559 HTTP 200",
                        size=18,
                    ),
                    text(
                        "cover-fact-c",
                        "43 route/content profiles × 3 viewports · 129/129",
                        size=18,
                    ),
                    text(
                        "cover-fact-d",
                        "62 token records · 52 component evidence records",
                        size=18,
                    ),
                ],
                gap=16,
                padding=32,
                fill="$color-surface-subtle",
            ),
            text(
                "cover-note",
                "Observed source values, normalized product mappings and accessibility corrections remain explicitly classified in DESIGN.md and the evidence register.",
                size=14,
                color="$color-text-muted",
            ),
        ],
        column=0,
        row=0,
        fill="$color-surface",
    )
    cover["metadata"] = {
        "type": "design-system-visualization",
        "normativeSource": "DESIGN.md",
        "generatedFrom": [
            "design-system/tokens.json",
            "design-system/components.json",
        ],
    }

    color_cards: list[dict[str, Any]] = []
    for row_index in range(0, len(color_names), 4):
        cards: list[dict[str, Any]] = []
        for name in color_names[row_index : row_index + 4]:
            hex_value = token_hex(tokens, name)
            text_color = (
                "$color-surface"
                if name
                in {
                    "primary",
                    "primary-dark",
                    "primary-active",
                    "text-on-accent",
                    "accent-accessible",
                    "accent-selected",
                    "text",
                    "text-muted",
                    "focus",
                    "danger",
                    "success",
                    "logo-olive",
                }
                else "$color-primary-active"
            )
            cards.append(
                frame(
                    f"color-card-{name}",
                    name,
                    [
                        text(
                            f"color-name-{name}",
                            name,
                            size=15,
                            weight=700,
                            color=text_color,
                        ),
                        text(
                            f"color-hex-{name}",
                            hex_value.upper(),
                            size=13,
                            color=text_color,
                        ),
                    ],
                    gap=8,
                    padding=18,
                    width="fill_container",
                    height=122,
                    fill=f"$color-{name}",
                    corner_radius="$radius-sm",
                )
            )
        color_cards.append(
            frame(
                f"color-row-{row_index // 4}",
                f"Color row {row_index // 4 + 1}",
                cards,
                layout="horizontal",
                gap=12,
                padding=0,
                fill="#00000000",
                corner_radius=0,
            )
        )

    colors = section(
        "colors",
        "Color tokens",
        "Raw observed values plus explicitly named normalized/accessibility roles",
        color_cards,
        column=1,
        row=0,
    )

    typography_rows: list[dict[str, Any]] = []
    for name in (
        "display-lg",
        "heading-xl",
        "heading-lg",
        "heading-md",
        "heading-sm",
        "body-lg",
        "body-md",
        "body-sm",
        "label",
        "caption",
    ):
        value = tokens["typography"][name]["$value"]
        size = round(float(value["fontSize"]["value"]) * 16)
        typography_rows.append(
            frame(
                f"type-row-{name}",
                name,
                [
                    text(
                        f"type-sample-{name}",
                        "Infrastructure with clarity",
                        size=size,
                        weight=int(value["fontWeight"]),
                        family=str(value["fontFamily"]),
                    ),
                    text(
                        f"type-meta-{name}",
                        f"{name} · {value['fontFamily']} · {size}px · {value['fontWeight']} / {value['lineHeight']}",
                        size=12,
                        color="$color-text-muted",
                    ),
                ],
                gap=6,
                padding=[14, 0],
                fill="#00000000",
                corner_radius=0,
            )
        )
    typography = section(
        "typography",
        "Typography",
        "Pragati Narrow for selected display/navigation contexts; Roboto for operational content",
        typography_rows,
        column=2,
        row=0,
    )

    spacing_rows: list[dict[str, Any]] = []
    for name in ("2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl"):
        px = token_px(tokens, "spacing", name)
        spacing_rows.append(
            frame(
                f"space-row-{name}",
                name,
                [
                    text(
                        f"space-label-{name}",
                        f"{name} · {px}px",
                        size=14,
                        weight=700,
                        width=110,
                    ),
                    {
                        "type": "rectangle",
                        "id": f"space-bar-{name}",
                        "name": f"{name} spacing bar",
                        "width": px * 6,
                        "height": 20,
                        "fill": "$color-accent",
                        "cornerRadius": "$radius-sm",
                    },
                ],
                layout="horizontal",
                gap=20,
                padding=10,
                fill="#00000000",
                corner_radius=0,
                alignItems="center",
            )
        )
    radius_cards = []
    for name in ("none", "sm", "md", "pill"):
        px = token_px(tokens, "rounded", name)
        radius_cards.append(
            frame(
                f"radius-{name}",
                name,
                [
                    text(
                        f"radius-label-{name}", f"{name}\n{px}px", size=14, weight=700
                    ),
                ],
                padding=20,
                width="fill_container",
                height=100,
                fill="$color-surface-muted",
                corner_radius=f"$radius-{name}",
            )
        )
    spacing = section(
        "spacing",
        "Spacing and radius",
        "Compact, square and information-dense production rhythm",
        [
            *spacing_rows,
            text("radius-heading", "Radius", size=22, weight=700),
            frame(
                "radius-row",
                "Radius tokens",
                radius_cards,
                layout="horizontal",
                gap=16,
                padding=0,
                fill="#00000000",
                corner_radius=0,
            ),
        ],
        column=0,
        row=1,
    )

    component_names = [
        "button-primary",
        "button-primary-hover",
        "button-primary-active",
        "button-primary-disabled",
        "button-secondary",
        "button-secondary-hover",
        "button-accent",
        "input-default",
        "input-focus",
        "input-disabled",
        "tag-default",
        "tag-selected",
        "status-neutral",
    ]
    component_nodes: list[dict[str, Any]] = []
    for name in component_names:
        component = components["components"][name]
        background_ref = component["backgroundColor"].strip("{}").replace("colors.", "")
        text_ref = (
            component.get("textColor", "{colors.text}")
            .strip("{}")
            .replace("colors.", "")
        )
        is_input = name.startswith("input-")
        node = frame(
            f"component-{name}",
            name,
            [
                text(
                    f"component-label-{name}",
                    "Example field" if is_input else name.replace("-", " ").title(),
                    size=14,
                    weight=700,
                    color=f"$color-{text_ref}",
                )
            ],
            layout="horizontal",
            padding=[12, 18],
            width=310,
            height=52,
            fill=f"$color-{background_ref}",
            corner_radius="$radius-md",
            alignItems="center",
            reusable=name in {"button-primary", "input-default", "tag-default"},
            stroke="$color-border"
            if name.startswith(("button-secondary", "input-"))
            else None,
            strokeWidth=1 if name.startswith(("button-secondary", "input-")) else 0,
        )
        component_nodes.append(node)
    component_rows = [
        frame(
            f"component-row-{index // 3}",
            f"Component row {index // 3 + 1}",
            component_nodes[index : index + 3],
            layout="horizontal",
            gap=16,
            padding=0,
            fill="#00000000",
            corner_radius=0,
        )
        for index in range(0, len(component_nodes), 3)
    ]
    components_section = section(
        "components",
        "Components and states",
        "Selected generated visual contracts; behavior contracts remain normative in DESIGN.md",
        component_rows,
        column=1,
        row=1,
    )

    evidence = section(
        "evidence",
        "Evidence boundary",
        "What this visual board does—and does not—claim",
        [
            frame(
                "evidence-observed",
                "Observed source evidence",
                [
                    text(
                        "evidence-observed-title",
                        "Observed source evidence",
                        size=22,
                        weight=700,
                        color="$color-surface",
                    ),
                    text(
                        "evidence-observed-copy",
                        "Public CSS declarations, exact live URLs/locations and visible computed samples are retained in the evidence register.",
                        size=16,
                        color="$color-surface",
                    ),
                ],
                gap=12,
                padding=28,
                fill="$color-primary",
                corner_radius="$radius-none",
            ),
            frame(
                "evidence-normalized",
                "Normalized product mapping",
                [
                    text(
                        "evidence-normalized-title",
                        "Normalized product mapping",
                        size=22,
                        weight=700,
                    ),
                    text(
                        "evidence-normalized-copy",
                        "Spacing, 44px controls, semantic roles and several component contracts are production decisions—not official source tokens.",
                        size=16,
                    ),
                ],
                gap=12,
                padding=28,
                fill="$color-surface-subtle",
            ),
            frame(
                "evidence-accessibility",
                "Accessibility correction",
                [
                    text(
                        "evidence-accessibility-title",
                        "Accessibility correction",
                        size=22,
                        weight=700,
                        color="$color-surface",
                    ),
                    text(
                        "evidence-accessibility-copy",
                        "accent-accessible #B15315 and text-on-accent #001C19 are scaffold corrections. Orange/white is not treated as normal-text AA.",
                        size=16,
                        color="$color-surface",
                    ),
                ],
                gap=12,
                padding=28,
                fill="$color-accent-accessible",
            ),
            frame(
                "evidence-limits",
                "Coverage limits",
                [
                    text(
                        "evidence-limits-title", "Coverage limits", size=22, weight=700
                    ),
                    text(
                        "evidence-limits-copy",
                        "559 means normalized route coverage units, not 559 authored templates. 10,666 sitemap URLs were discovered, not manually browser-rendered one by one.",
                        size=16,
                    ),
                ],
                gap=12,
                padding=28,
                fill="$color-table-header",
            ),
            text(
                "evidence-links",
                "Normative source: DESIGN.md\nGenerated contracts: design-system/\nHuman evidence register: docs/design-system/source-evidence.md",
                size=15,
                color="$color-text-muted",
            ),
        ],
        column=2,
        row=1,
    )

    return {
        "version": "2.17",
        "variables": variables,
        "children": [cover, colors, typography, spacing, components_section, evidence],
    }


def render() -> str:
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    components = json.loads(COMPONENTS_PATH.read_text(encoding="utf-8"))
    return (
        json.dumps(build_document(tokens, components), ensure_ascii=False, indent=2)
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export the pen.dev visual design-system board"
    )
    parser.add_argument(
        "--check", action="store_true", help="Fail if the generated board has drifted"
    )
    args = parser.parse_args()
    expected = render()
    if args.check:
        if (
            not OUTPUT_PATH.exists()
            or OUTPUT_PATH.read_text(encoding="utf-8") != expected
        ):
            print(f"Drift detected: {OUTPUT_PATH.relative_to(ROOT)}")
            return 1
        print(f"Verified pen.dev board: {OUTPUT_PATH.relative_to(ROOT)}")
        return 0
    OUTPUT_PATH.write_text(expected, encoding="utf-8")
    print(f"Generated pen.dev board: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
