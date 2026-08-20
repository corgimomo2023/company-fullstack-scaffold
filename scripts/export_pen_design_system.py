from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "DESIGN.md"
TOKENS_PATH = ROOT / "design-system" / "tokens.json"
COMPONENTS_PATH = ROOT / "design-system" / "components.json"
SOURCE_SPECIMENS_PATH = ROOT / "design-system" / "source-component-specimens.json"
SOURCE_EVIDENCE_INDEX_PATH = (
    ROOT / "docs" / "design-system" / "evidence" / "source-evidence-index.json"
)
OUTPUT_PATH = ROOT / "design-system" / "asia-allied-design-system.pen"

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1240

PUBLIC_SPECIMEN_KINDS = {
    "site-header": "navigation",
    "utility-navigation": "navigation",
    "site-search": "search",
    "desktop-navigation": "navigation",
    "mobile-navigation": "dropdown",
    "breadcrumbs": "breadcrumb",
    "page-title": "rich-text",
    "page-menu": "navigation",
    "page-tabs": "tabs",
    "filter-bar": "select",
    "hero-carousel": "carousel",
    "image-title-card": "card",
    "image-card": "card",
    "image-overlay-card": "media-card",
    "overlay-cover-card": "media-card",
    "image-plate": "card",
    "spaced-image-plate": "card",
    "left-image-card": "media-card",
    "top-image-card": "media-card",
    "blog-card-list": "media-card",
    "thumbnail-list": "media-card",
    "information-tile-card": "card",
    "image-slider": "carousel",
    "milestone-card": "timeline",
    "share-dropdown": "dropdown",
    "feature-slider": "carousel",
    "video-link": "media-card",
    "rich-text": "rich-text",
    "tag-filter": "tag",
    "custom-select": "select",
    "listing-table": "table",
    "pagination": "pagination",
    "load-more": "load-more",
    "button": "button-states",
    "text-input": "input",
    "checkbox-radio": "checkbox",
    "validation": "field",
    "form-group": "field",
    "subscription-form": "form",
    "contact-form": "form",
    "year-accordion": "accordion",
    "development-timeline": "timeline",
    "corporate-structure": "timeline",
    "global-footprint-map": "map",
    "document-download": "download",
    "director-person": "not-observed",
    "job-listing": "card",
    "publication": "not-observed",
    "project-list-detail": "not-observed",
    "social-links": "social-links",
    "back-to-top": "back-to-top",
    "footer": "navigation",
}
GUTTER = 40
BOARD_COLUMNS = 5

BEHAVIOR_GROUPS = {
    "Behavior · actions and navigation": [
        "button",
        "icon-button",
        "link",
        "tag-filter",
        "pagination",
        "tabs",
        "navigation",
        "breadcrumb",
        "dropdown-menu",
    ],
    "Behavior · forms and selection": [
        "text-input",
        "textarea",
        "select",
        "checkbox",
        "radio",
        "field",
        "search",
    ],
    "Behavior · content and data": [
        "card",
        "media-card",
        "metric-card",
        "table",
        "accordion",
        "carousel",
        "timeline",
        "map",
        "file-download",
    ],
    "Behavior · feedback and system": [
        "status-badge",
        "dialog",
        "alert",
        "toast",
        "empty-state",
        "loading-skeleton",
    ],
}

VISUAL_GROUPS = {
    "Visual contracts · actions and forms": [
        "button-primary",
        "button-primary-hover",
        "button-primary-active",
        "button-primary-disabled",
        "button-secondary",
        "button-secondary-hover",
        "button-secondary-disabled",
        "button-accent",
        "navigation-active",
        "input-default",
        "input-focus",
        "input-disabled",
        "tag-default",
        "tag-selected",
        "focus-indicator",
    ],
    "Visual contracts · surfaces and status": [
        "card-default",
        "card-selected",
        "page-canvas",
        "panel-muted",
        "table-header",
        "table-row-selected",
        "metadata",
        "status-success",
        "status-danger",
        "status-warning",
        "status-neutral",
        "section-accent-rule",
        "accent-surface-large",
        "divider",
        "logo-orange-swatch",
        "logo-olive-swatch",
    ],
}

COLOR_ROLES = {
    "primary": (
        "Primary actions, links and active navigation",
        "normalized observed value",
        "Use for structural action hierarchy",
    ),
    "primary-dark": (
        "Hover and dense navigation framing",
        "normalized observed value",
        "Use for stronger green separation",
    ),
    "primary-active": (
        "Active and pressed separation",
        "normalized observed state",
        "Reserve for active/pressed state",
    ),
    "accent": (
        "Rules, charts and non-text emphasis",
        "normalized observed value",
        "Never use normal white text on this fill",
    ),
    "accent-accessible": (
        "White-text orange interaction surface",
        "accessibility correction",
        "Use when orange must carry normal white text",
    ),
    "accent-selected": (
        "Selected warning/tag surface",
        "normalized observed value",
        "Pair with white label and non-color cue",
    ),
    "text-on-accent": (
        "Dark text on raw accent",
        "accessibility correction",
        "Use on #E6762D for normal text",
    ),
    "text": (
        "Primary interface and body text",
        "normalized observed value",
        "Default text on light surfaces",
    ),
    "text-muted": (
        "Secondary metadata",
        "normalized observed value",
        "Use on white only",
    ),
    "surface": (
        "Main surface and cards",
        "normalized observed value",
        "Base foreground surface",
    ),
    "surface-subtle": (
        "Page canvas and alternate rows",
        "normalized observed value",
        "Use for low-emphasis regions",
    ),
    "surface-muted": (
        "Muted structural regions",
        "normalized observed value",
        "Use for rails and grouped regions",
    ),
    "surface-disabled": (
        "Disabled controls",
        "normalized observed value",
        "Always pair with disabled semantics",
    ),
    "border": (
        "Dividers and control boundaries",
        "normalized observed value",
        "Not a text color; reinforce interactive focus",
    ),
    "table-header": (
        "Warm table/list header tint",
        "normalized observed value",
        "Use behind dark table headings",
    ),
    "focus": (
        "Focus-visible indicator",
        "normalized product role",
        "Never remove without equivalent indicator",
    ),
    "danger": (
        "Error/destructive text and borders",
        "observed shared-layer value",
        "Pair with text/icon; never color alone",
    ),
    "success": (
        "Positive state",
        "normalized product role",
        "Pair with explicit success label/icon",
    ),
    "logo-orange": (
        "Approved brand-mark color only",
        "observed logo sample",
        "Do not use as product status/control",
    ),
    "logo-olive": (
        "Approved brand-mark color only",
        "observed logo sample",
        "Do not use as product status/control",
    ),
}

CONTRAST_PAIRS = [
    (
        "white-primary",
        "White / primary",
        "6.48:1",
        True,
        "$color-primary",
        "$color-surface",
    ),
    (
        "white-primary-dark",
        "White / primary-dark",
        "13.52:1",
        True,
        "$color-primary-dark",
        "$color-surface",
    ),
    (
        "white-accent",
        "White / accent",
        "3.00:1",
        False,
        "$color-accent",
        "$color-surface",
    ),
    (
        "white-accent-accessible",
        "White / accessible accent",
        "5.10:1",
        True,
        "$color-accent-accessible",
        "$color-surface",
    ),
    (
        "white-accent-selected",
        "White / selected accent",
        "9.59:1",
        True,
        "$color-accent-selected",
        "$color-surface",
    ),
    ("text-white", "Text / white", "12.63:1", True, "$color-surface", "$color-text"),
    (
        "text-muted-white",
        "Muted text / white",
        "4.69:1",
        True,
        "$color-surface",
        "$color-text-muted",
    ),
    (
        "danger-white",
        "Danger / white",
        "4.53:1",
        True,
        "$color-surface",
        "$color-danger",
    ),
]

PAGE_PATTERNS = [
    ("home", "Home", "Brand overview and entry points"),
    ("group", "Group", "Corporate narrative and governance"),
    (
        "investor-static",
        "Investor static",
        "Reports, governance, chart and calendar destinations",
    ),
    ("publication-list", "Publication list", "Archives, filters and pagination"),
    (
        "publication-detail",
        "Publication detail",
        "Article/document metadata and download",
    ),
    ("project-sector", "Project sector", "Sector landing and project discovery"),
    ("project-list", "Project list", "Filterable/listed project collection"),
    ("project-detail", "Project detail", "Media, facts and related content"),
    ("job", "Job", "Vacancy listing and detail"),
    ("form", "Form", "Contact/application controls and validation"),
    ("legal", "Legal", "Policy and long-form prose"),
]


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
    letter_spacing: float = 0,
) -> dict[str, Any]:
    value = {
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
    if letter_spacing:
        value["letterSpacing"] = letter_spacing
    return value


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


def rectangle(
    node_id: str,
    name: str,
    *,
    width: int | str,
    height: int,
    fill: str,
    corner_radius: int | str = 0,
) -> dict[str, Any]:
    return {
        "type": "rectangle",
        "id": node_id,
        "name": name,
        "width": width,
        "height": height,
        "fill": fill,
        "cornerRadius": corner_radius,
    }


def row(
    node_id: str,
    name: str,
    children: list[dict[str, Any]],
    *,
    gap: int = 12,
) -> dict[str, Any]:
    return frame(
        node_id,
        name,
        children,
        layout="horizontal",
        gap=gap,
        padding=0,
        fill="#00000000",
        corner_radius=0,
    )


def section(
    node_id: str,
    name: str,
    subtitle: str,
    body: list[dict[str, Any]],
    *,
    index: int,
    fill: str = "$color-surface",
) -> dict[str, Any]:
    column = index % BOARD_COLUMNS
    board_row = index // BOARD_COLUMNS
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
        gap=18,
        padding=40,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        fill=fill,
        clip=True,
        x=column * (CANVAS_WIDTH + GUTTER),
        y=board_row * (CANVAS_HEIGHT + GUTTER),
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
    return str(tokens["color"][name]["$value"]["hex"])


def token_px(tokens: dict[str, Any], group: str, name: str) -> int:
    return int(tokens[group][name]["$value"]["value"])


def token_items(tokens: dict[str, Any], group: str) -> list[tuple[str, dict[str, Any]]]:
    return [
        (name, value)
        for name, value in tokens[group].items()
        if not name.startswith("$")
    ]


def color_name(reference: str | None, fallback: str = "surface") -> str:
    if not reference:
        return fallback
    return reference.strip("{}").removeprefix("colors.")


def compact_list(values: list[str], limit: int = 3) -> str:
    if len(values) <= limit:
        return ", ".join(values)
    return f"{', '.join(values[:limit])} +{len(values) - limit}"


def source_control(
    node_id: str,
    label: str,
    *,
    fill: str = "#FFFFFF",
    color: str = "#333333",
    width: int | str = "fill_container",
    height: int = 40,
    border: str = "#C7C7C7",
    radius: int = 0,
) -> dict[str, Any]:
    return frame(
        node_id,
        label,
        [text(f"{node_id}-label", label, size=14, weight=700, color=color)],
        layout="horizontal",
        padding=[10, 14],
        width=width,
        height=height,
        fill=fill,
        corner_radius=radius,
        stroke=border,
        strokeWidth=1,
        alignItems="center",
    )


def source_specimen_visual(name: str, kind: str) -> list[dict[str, Any]]:
    """Build editable topology from audited source DOM/CSS, never a screenshot."""
    if kind == "button-states":
        return [
            row(
                f"source-{name}-primary-row",
                "Contact submit states",
                [
                    source_control(
                        f"source-{name}-default",
                        "SUBMIT · DEFAULT",
                        fill="#E6762D",
                        color="#FFFFFF",
                        height=54,
                        border="#E6762D",
                    ),
                    source_control(
                        f"source-{name}-hover",
                        "SUBMIT · HOVER",
                        fill="#DF681B",
                        color="#FFFFFF",
                        height=54,
                        border="#E6762D",
                    ),
                    source_control(
                        f"source-{name}-focus",
                        "FOCUS",
                        fill="#DF681B",
                        color="#FFFFFF",
                        height=54,
                        border="#E6762D",
                    ),
                    source_control(
                        f"source-{name}-active",
                        "ACTIVE = HOVER¹",
                        fill="#DF681B",
                        color="#FFFFFF",
                        height=54,
                        border="#E6762D",
                    ),
                ],
                gap=8,
            ),
            row(
                f"source-{name}-reset-row",
                "Contact reset states",
                [
                    source_control(
                        f"source-{name}-reset-default",
                        "RESET · DEFAULT",
                        color="#E6762D",
                        height=46,
                        border="#FFFFFF",
                    ),
                    source_control(
                        f"source-{name}-reset-hover",
                        "RESET · HOVER / FOCUS",
                        fill="#EFEFEF",
                        color="#E6762D",
                        height=46,
                        border="#FFFFFF",
                    ),
                ],
                gap=8,
            ),
        ]
    if kind == "pagination":
        return [
            row(
                f"source-{name}-row",
                "Actual pagination anatomy",
                [
                    text(
                        f"source-{name}-previous",
                        "‹",
                        size=22,
                        color="#E6762D",
                        width=24,
                    ),
                    text(
                        f"source-{name}-page-1",
                        "1",
                        size=18,
                        color="#707070",
                        width=24,
                    ),
                    text(
                        f"source-{name}-page-2-current",
                        "2",
                        size=18,
                        weight=700,
                        color="#E6762D",
                        width=24,
                    ),
                    source_control(
                        f"source-{name}-page-input",
                        "3",
                        width=38,
                        height=30,
                        color="#707070",
                        border="#E6762D",
                    ),
                    text(
                        f"source-{name}-total",
                        "/ 12",
                        size=18,
                        color="#707070",
                        width=46,
                    ),
                    text(
                        f"source-{name}-next",
                        "›",
                        size=22,
                        color="#E6762D",
                        width=24,
                    ),
                ],
                gap=10,
            )
        ]
    if kind in {"back-to-top", "icon-button"}:
        return [
            row(
                f"source-{name}-states",
                "Back-to-top",
                [
                    source_control(
                        f"source-{name}-default", "↑  TOP", width=86, fill="#CECECE"
                    ),
                    source_control(
                        f"source-{name}-hover", "↑  TOP", width=86, fill="#CECECE"
                    ),
                ],
            )
        ]
    if kind == "link":
        return [
            source_control(
                f"source-{name}-default",
                "Investor Relations",
                fill="#003531",
                color="#FFFFFF",
                border="#003531",
            ),
            source_control(
                f"source-{name}-hover",
                "Investor Relations · hover",
                fill="#DFDEDE",
                color="#006A63",
                border="#DFDEDE",
            ),
        ]
    if kind == "tag":
        return [
            row(
                f"source-{name}-states",
                "Tags",
                [
                    source_control(
                        f"source-{name}-default",
                        "ALL · LIVE SELECTED",
                        width=170,
                        fill="#E6762D",
                        color="#FFFFFF",
                        border="#E6762D",
                    ),
                    source_control(
                        f"source-{name}-hover",
                        "ESG · HOVER",
                        width=125,
                        fill="#733208",
                        color="#FFFFFF",
                        border="#733208",
                    ),
                ],
            )
        ]
    if kind == "select":
        return [
            row(
                f"source-{name}-layout",
                "Custom select open state",
                [
                    source_control(
                        f"source-{name}-trigger",
                        "2026    ▾",
                        fill="#FFFFFF",
                        border="#FFFFFF",
                    ),
                    frame(
                        f"source-{name}-menu",
                        "Open options",
                        [
                            text(
                                f"source-{name}-option-a",
                                "2026",
                                size=14,
                                color="#FFFFFF",
                            ),
                            frame(
                                f"source-{name}-option-hover",
                                "Hovered option",
                                [
                                    text(
                                        f"source-{name}-option-b",
                                        "2025",
                                        size=14,
                                        color="#FFFFFF",
                                    )
                                ],
                                padding=8,
                                fill="#E6762D",
                                corner_radius=0,
                            ),
                            text(
                                f"source-{name}-option-c",
                                "2024",
                                size=14,
                                color="#FFFFFF",
                            ),
                        ],
                        gap=5,
                        padding=8,
                        fill="#006A63",
                        corner_radius=0,
                    ),
                ],
            )
        ]
    if kind in {"input", "textarea"}:
        height = 82 if kind == "textarea" else 42
        label = {"input": "First Name", "textarea": "Message"}[kind]
        return [
            row(
                f"source-{name}-states",
                "Default and focus",
                [
                    source_control(
                        f"source-{name}-default", label, fill="#F7F7F7", height=height
                    ),
                    source_control(
                        f"source-{name}-state",
                        f"{label} · FOCUS",
                        fill="#FFFFFF",
                        height=height,
                        border="#80BDFF",
                    ),
                ],
            )
        ]
    if kind in {"checkbox", "radio"}:
        off = "□" if kind == "checkbox" else "○"
        on = "■" if kind == "checkbox" else "●"
        return [
            text(f"source-{name}-unchecked", f"{off}  Option unchecked", size=16),
            text(
                f"source-{name}-checked",
                f"{on}  Option checked",
                size=16,
                color="#006A63",
            ),
            text(
                f"source-{name}-css-only",
                "CSS reference fixture · live DOM not observed",
                size=11,
                color="#B15315",
            ),
        ]
    if kind == "field":
        return [
            row(
                f"source-{name}-row",
                "Contact field",
                [
                    text(f"source-{name}-label", "First Name *", size=16, width=155),
                    source_control(f"source-{name}-control", "", fill="#F7F7F7"),
                ],
            )
        ]
    if kind == "search":
        return [
            frame(
                f"source-{name}-open",
                "Open site search",
                [
                    row(
                        f"source-{name}-form",
                        "Search form",
                        [
                            source_control(
                                f"source-{name}-input",
                                "Search",
                                fill="#006A63",
                                color="#FFFFFF",
                                border="#FFFFFF",
                            ),
                            source_control(
                                f"source-{name}-submit",
                                "⌕",
                                width=44,
                                fill="#006A63",
                                color="#FFFFFF",
                                border="#FFFFFF",
                            ),
                        ],
                    )
                ],
                padding=16,
                fill="#006A63",
                corner_radius=0,
            )
        ]
    if kind in {"card", "media-card"}:
        return [
            row(
                f"source-{name}-layout",
                "Source card",
                [
                    rectangle(
                        f"source-{name}-image",
                        "Source image ratio",
                        width=150,
                        height=112,
                        fill="#AAAAAA",
                    ),
                    frame(
                        f"source-{name}-copy",
                        "Card copy",
                        [
                            text(
                                f"source-{name}-title",
                                "Building a sustainable future",
                                size=18,
                                weight=700,
                            ),
                            text(
                                f"source-{name}-meta",
                                "18 Aug 2026 · AAI",
                                size=12,
                                color="#707070",
                            ),
                            text(
                                f"source-{name}-link",
                                "READ MORE →",
                                size=13,
                                weight=700,
                                color="#006A63",
                            ),
                        ],
                        padding=14,
                        fill="#FFFFFF",
                        corner_radius=0,
                    ),
                ],
            )
        ]
    if kind == "table":
        return [
            frame(
                f"source-{name}-table",
                "CSS table fixture",
                [
                    row(
                        f"source-{name}-head",
                        "Table header",
                        [
                            text(f"source-{name}-h1", "POSITION", size=12, weight=700),
                            text(f"source-{name}-h2", "LOCATION", size=12, weight=700),
                        ],
                    ),
                    row(
                        f"source-{name}-r1",
                        "Table row",
                        [
                            text(f"source-{name}-c1", "Project Manager", size=13),
                            text(f"source-{name}-c2", "Hong Kong", size=13),
                        ],
                    ),
                ],
                padding=12,
                fill="#FFF2EA",
                corner_radius=0,
            )
        ]
    if kind == "tabs":
        return [
            row(
                f"source-{name}-desktop",
                "Projects tabs",
                [
                    text(
                        f"source-{name}-all",
                        "ALL",
                        size=17,
                        weight=700,
                        color="#E6762D",
                    ),
                    text(
                        f"source-{name}-building",
                        "BUILDING",
                        size=17,
                        weight=700,
                        color="#707070",
                    ),
                    text(
                        f"source-{name}-civil",
                        "CIVIL ENGINEERING",
                        size=17,
                        weight=700,
                        color="#707070",
                    ),
                ],
                gap=24,
            ),
            rectangle(
                f"source-{name}-rule",
                "Orange bottom rule",
                width="fill_container",
                height=1,
                fill="#E6762D",
            ),
            source_control(
                f"source-{name}-mobile",
                "ALL PROJECTS       ▾",
                height=37,
                color="#707070",
                border="#E6762D",
            ),
        ]
    if kind == "accordion":
        return [
            source_control(
                f"source-{name}-collapsed",
                "2020s   A Step Further                         ＋",
                height=54,
                fill="#FFFFFF",
            ),
            frame(
                f"source-{name}-expanded",
                "Expanded year",
                [
                    text(
                        f"source-{name}-expanded-title",
                        "2010s   Stand High Look Far                  −",
                        size=17,
                        weight=700,
                    ),
                    text(
                        f"source-{name}-expanded-copy",
                        "2016  Major development milestone",
                        size=13,
                    ),
                ],
                padding=14,
                fill="#F7F7F7",
                corner_radius=0,
            ),
        ]
    if kind == "navigation":
        return [
            frame(
                f"source-{name}-desktop",
                "Desktop primary navigation",
                [
                    row(
                        f"source-{name}-items",
                        "Navigation items",
                        [
                            text(
                                f"source-{name}-group",
                                "THE GROUP",
                                size=14,
                                color="#FFFFFF",
                            ),
                            text(
                                f"source-{name}-business",
                                "GROUP BUSINESS",
                                size=14,
                                color="#FFFFFF",
                            ),
                            text(
                                f"source-{name}-ir",
                                "INVESTOR RELATIONS",
                                size=14,
                                color="#FFFFFF",
                            ),
                        ],
                    )
                ],
                padding=16,
                fill="#003531",
                corner_radius=0,
            )
        ]
    if kind == "breadcrumb":
        return [
            text(
                f"source-{name}-trail",
                "AAI  /  The Group  /  Development History",
                size=14,
                color="#006A63",
            )
        ]
    if kind == "dropdown":
        return [
            frame(
                f"source-{name}-open",
                "Open level-2 navigation",
                [
                    text(
                        f"source-{name}-a", "About the Group", size=16, color="#FFFFFF"
                    ),
                    text(
                        f"source-{name}-b",
                        "Corporate Structure",
                        size=16,
                        color="#FFFFFF",
                    ),
                    text(f"source-{name}-c", "Directors", size=16, color="#FFFFFF"),
                ],
                gap=10,
                padding=14,
                fill="#003531",
                corner_radius=0,
                stroke="#E6762D",
                strokeWidth=4,
            )
        ]
    if kind == "carousel":
        return [
            frame(
                f"source-{name}-slide",
                "Hero carousel slide",
                [
                    text(
                        f"source-{name}-headline",
                        "A STEP FURTHER",
                        size=26,
                        weight=700,
                        color="#FFFFFF",
                    ),
                    text(
                        f"source-{name}-sub",
                        "Building a better future",
                        size=15,
                        color="#FFFFFF",
                    ),
                    row(
                        f"source-{name}-controls",
                        "Carousel controls",
                        [
                            text(
                                f"source-{name}-prev",
                                "‹",
                                size=24,
                                color="#FFFFFF",
                                width=30,
                            ),
                            text(
                                f"source-{name}-dots",
                                "●  ○  ○",
                                size=14,
                                color="#FFFFFF",
                                width=80,
                            ),
                            text(
                                f"source-{name}-pause",
                                "Ⅱ",
                                size=18,
                                color="#FFFFFF",
                                width=30,
                            ),
                            text(
                                f"source-{name}-next",
                                "›",
                                size=24,
                                color="#FFFFFF",
                                width=30,
                            ),
                        ],
                    ),
                ],
                padding=18,
                fill="#006A63",
                corner_radius=0,
            )
        ]
    if kind == "timeline":
        return [
            row(
                f"source-{name}-years",
                "Development timeline",
                [
                    text(
                        f"source-{name}-y1",
                        "●\n1968",
                        size=16,
                        weight=700,
                        color="#E6762D",
                        width=70,
                    ),
                    rectangle(
                        f"source-{name}-line",
                        "Timeline line",
                        width="fill_container",
                        height=1,
                        fill="#DBDBDB",
                    ),
                    text(
                        f"source-{name}-y2",
                        "●\n2020",
                        size=16,
                        weight=700,
                        color="#E6762D",
                        width=70,
                    ),
                ],
            )
        ]
    if kind == "map":
        return [
            frame(
                f"source-{name}-surface",
                "Global footprint map",
                [
                    text(
                        f"source-{name}-hk",
                        "● Hong Kong",
                        size=13,
                        weight=700,
                        color="#E6762D",
                    ),
                    text(
                        f"source-{name}-cn",
                        "             ● Mainland China",
                        size=13,
                        weight=700,
                        color="#733208",
                    ),
                    text(
                        f"source-{name}-au",
                        "                          ● Australia",
                        size=13,
                        weight=700,
                        color="#E6762D",
                    ),
                ],
                padding=18,
                fill="#F7F7F7",
                corner_radius=0,
            )
        ]
    if kind == "rich-text":
        return [
            text(
                f"source-{name}-heading",
                "Building a sustainable future",
                size=20,
                weight=700,
                color="#006A63",
            ),
            text(
                f"source-{name}-body",
                "Structured article copy with links, lists and media.",
                size=13,
                color="#333333",
            ),
            text(
                f"source-{name}-link",
                "Read the full story →",
                size=13,
                weight=700,
                color="#E6762D",
            ),
        ]
    if kind == "form":
        return [
            row(
                f"source-{name}-fields",
                "Form fields",
                [
                    source_control(
                        f"source-{name}-email", "Email address", fill="#F7F7F7"
                    ),
                    source_control(
                        f"source-{name}-submit",
                        "SUBMIT",
                        width=110,
                        fill="#E6762D",
                        color="#FFFFFF",
                        border="#E6762D",
                    ),
                ],
            ),
            text(
                f"source-{name}-note",
                "Required fields · validation · anti-abuse area",
                size=11,
                color="#707070",
            ),
        ]
    if kind == "social-links":
        return [
            row(
                f"source-{name}-icons",
                "Social actions",
                [
                    source_control(
                        f"source-{name}-facebook",
                        "f",
                        width=42,
                        height=42,
                        fill="#006A63",
                        color="#FFFFFF",
                        border="#006A63",
                    ),
                    source_control(
                        f"source-{name}-linkedin",
                        "in",
                        width=42,
                        height=42,
                        fill="#006A63",
                        color="#FFFFFF",
                        border="#006A63",
                    ),
                    source_control(
                        f"source-{name}-video",
                        "▶",
                        width=42,
                        height=42,
                        fill="#006A63",
                        color="#FFFFFF",
                        border="#006A63",
                    ),
                ],
            )
        ]
    if kind == "load-more":
        return [
            source_control(
                f"source-{name}-default",
                "LOAD MORE",
                width=150,
                height=48,
                fill="#FFFFFF",
                color="#E6762D",
                border="#E6762D",
            )
        ]
    if kind == "download":
        return [
            source_control(
                f"source-{name}-item",
                "↓   Annual Report 2025   PDF",
                height=52,
                fill="#FFFFFF",
                color="#006A63",
            )
        ]
    raise ValueError(f"Unknown source specimen kind: {kind}")


def source_specimen_card(
    name: str,
    specification: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    canvas = frame(
        f"source-specimen-{name}-canvas",
        f"Editable {name} specimen",
        source_specimen_visual(name, str(specification["kind"])),
        gap=8,
        padding=14,
        height=174,
        fill="$color-surface-subtle",
        corner_radius=0,
        clip=True,
    )
    mode = str(specification.get("sourceMode", "live-observed"))
    card = frame(
        f"source-specimen-{name}",
        name,
        [
            text(f"source-specimen-{name}-title", name.upper(), size=18, weight=700),
            canvas,
            text(
                f"source-specimen-{name}-selector",
                f"Selector · {specification['selector']}",
                size=10,
                color="$color-text-muted",
            ),
            text(
                f"source-specimen-{name}-states",
                f"Observed · {compact_list(list(specification['observedStates']), 4)}",
                size=10,
                color="$color-text-muted",
            ),
        ],
        gap=7,
        padding=14,
        height=298,
        fill="$color-surface",
        corner_radius=0,
        stroke="$color-border",
        strokeWidth=1,
        clip=True,
    )
    card["metadata"] = {
        "contractName": name,
        "sourceMode": mode,
        "sourceComponents": contract["evidence"]["sourceComponents"],
        "sourceUrls": contract["evidence"]["sourceUrls"],
        "selector": specification["selector"],
        "defaultStyles": specification["defaultStyles"],
        "observedStates": specification["observedStates"],
        "editable": True,
        "notScreenshot": True,
    }
    return card


def source_exclusion_card(name: str, contract: dict[str, Any]) -> dict[str, Any]:
    card = frame(
        f"source-exclusion-{name}",
        f"Excluded normalized contract: {name}",
        [
            text(f"source-exclusion-{name}-title", name.upper(), size=18, weight=700),
            text(
                f"source-exclusion-{name}-copy",
                "NOT A SOURCE COMPONENT\nNormalized product contract; no exact live-site specimen is claimed.",
                size=13,
                color="$color-danger",
            ),
            text(
                f"source-exclusion-{name}-sources",
                f"Related markers · {compact_list(contract['evidence']['sourceComponents'])}",
                size=10,
                color="$color-text-muted",
            ),
        ],
        gap=12,
        padding=18,
        height=298,
        fill="$color-surface-subtle",
        corner_radius=0,
        stroke="$color-danger",
        strokeWidth=1,
    )
    card["metadata"] = {
        "contractName": name,
        "sourceMode": "normalized-not-source-component",
        "sourceComponents": contract["evidence"]["sourceComponents"],
        "sourceUrls": contract["evidence"]["sourceUrls"],
    }
    return card


def source_component_boards(
    source_specimens: dict[str, Any],
    contracts: dict[str, Any],
    start_index: int,
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    specimens = source_specimens["components"]
    normalized = {
        name
        for name, contract in contracts.items()
        if contract["evidence"]["classification"] == "normalized-product"
    }
    expected = set(contracts) - normalized
    if set(specimens) != expected:
        raise ValueError(
            f"Source specimen coverage drift: {sorted(set(specimens) ^ expected)}"
        )
    for name, contract in contracts.items():
        if name in specimens:
            cards.append(source_specimen_card(name, specimens[name], contract))
        else:
            cards.append(source_exclusion_card(name, contract))

    boards: list[dict[str, Any]] = []
    board_sizes = [6, 5, 5, 5, 5, 5]
    if sum(board_sizes) != len(cards):
        raise ValueError(f"Source library board partition drift: {len(cards)} cards")
    cursor = 0
    for board_offset, board_size in enumerate(board_sizes):
        batch = cards[cursor : cursor + board_size]
        cursor += board_size
        rows = [
            row(
                f"source-library-{board_offset}-row-{row_index}",
                "Source specimen row",
                batch[row_index * 2 : row_index * 2 + 2],
                gap=16,
            )
            for row_index in range((len(batch) + 1) // 2)
        ]
        boards.append(
            section(
                f"source-library-{board_offset + 1}",
                f"Source component library · {board_offset + 1}",
                "Editable exact-source specimens · live, CSS-reference and normalized exclusions are separated",
                rows,
                index=start_index + board_offset,
            )
        )
    return boards


def public_specimen_card(name: str, record: dict[str, Any]) -> dict[str, Any]:
    classification = str(record["classification"])
    mode = {
        "observed-dom-and-css": "live-observed",
        "observed-css-only": "css-reference",
        "not-observed": "not-observed",
    }[classification]
    selectors = [
        selector
        for item in record["css_selector_evidence"]
        for selector in item["selectors"]
    ]
    selector_copy = compact_list(selectors or record["markers"], 2)
    states = sorted(record["state_evidence"])
    visual: list[dict[str, Any]]
    if mode == "not-observed":
        visual = [
            text(
                f"public-{name}-not-observed",
                "NOT OBSERVED · no editable source specimen is claimed",
                size=13,
                weight=700,
                color="$color-danger",
            )
        ]
    else:
        visual = source_specimen_visual(
            f"public-{name}", str(PUBLIC_SPECIMEN_KINDS[name])
        )
        if mode == "css-reference":
            visual.append(
                text(
                    f"public-{name}-css-reference",
                    "CSS REFERENCE FIXTURE · live DOM not verified",
                    size=10,
                    weight=700,
                    color="#B15315",
                )
            )
    canvas = frame(
        f"public-specimen-{name}-canvas",
        f"Editable public-site {name} example",
        visual,
        gap=7,
        padding=12,
        height=164,
        fill="$color-surface-subtle",
        corner_radius=0,
        clip=True,
    )
    card = frame(
        f"public-specimen-{name}",
        name,
        [
            row(
                f"public-specimen-{name}-heading",
                "Component and evidence class",
                [
                    text(
                        f"public-specimen-{name}-title",
                        name.upper(),
                        size=17,
                        weight=700,
                    ),
                    text(
                        f"public-specimen-{name}-mode",
                        mode.upper(),
                        size=10,
                        weight=700,
                        color=(
                            "$color-danger" if mode == "not-observed" else "#006A63"
                        ),
                        width=150,
                    ),
                ],
            ),
            canvas,
            text(
                f"public-specimen-{name}-anatomy",
                f"Anatomy · {compact_list(record['markers'], 3)}",
                size=10,
                color="$color-text-muted",
            ),
            text(
                f"public-specimen-{name}-selector",
                f"Selector · {selector_copy}",
                size=10,
                color="$color-text-muted",
            ),
            text(
                f"public-specimen-{name}-states",
                f"Observed states · {compact_list(states, 4) if states else 'not observed'}",
                size=10,
                color="$color-text-muted",
            ),
        ],
        gap=7,
        padding=16,
        height=330,
        fill="$color-surface",
        corner_radius=0,
        stroke=("$color-danger" if mode == "not-observed" else "$color-border"),
        strokeWidth=1,
    )
    card["metadata"] = {
        "sourceFamily": name,
        "sourceMode": mode,
        "classification": classification,
        "kind": PUBLIC_SPECIMEN_KINDS[name],
        "primaryEvidenceUrl": record["primary_evidence_url"],
        "markers": record["markers"],
        "selectors": selectors,
        "stateEvidence": record["state_evidence"],
        "livePageLocations": record["live_page_locations"],
        "cssSelectorEvidence": record["css_selector_evidence"],
    }
    return card


def public_component_catalogue_boards(
    public_components: dict[str, Any], start_index: int
) -> list[dict[str, Any]]:
    if set(public_components) != set(PUBLIC_SPECIMEN_KINDS):
        raise ValueError(
            "Public component catalogue drift: "
            f"{sorted(set(public_components) ^ set(PUBLIC_SPECIMEN_KINDS))}"
        )
    cards = [
        public_specimen_card(name, record) for name, record in public_components.items()
    ]
    board_sizes = [6, 6, 6, 6, 6, 6, 6, 6, 4]
    if sum(board_sizes) != len(cards):
        raise ValueError(f"Public catalogue board partition drift: {len(cards)} cards")
    boards: list[dict[str, Any]] = []
    cursor = 0
    for board_offset, board_size in enumerate(board_sizes):
        batch = cards[cursor : cursor + board_size]
        cursor += board_size
        rows = [
            row(
                f"public-catalogue-{board_offset}-row-{row_index}",
                "Public source family row",
                batch[row_index * 2 : row_index * 2 + 2],
                gap=16,
            )
            for row_index in range((len(batch) + 1) // 2)
        ]
        boards.append(
            section(
                f"public-catalogue-{board_offset + 1}",
                f"Public component catalogue · {board_offset + 1}",
                "Material-style examples · anatomy · selectors · observed states · evidence class",
                rows,
                index=start_index + board_offset,
            )
        )
    return boards


def color_board(tokens: dict[str, Any], index: int) -> dict[str, Any]:
    dark_text = {
        "accent",
        "text-on-accent",
        "surface",
        "surface-subtle",
        "surface-muted",
        "surface-disabled",
        "border",
        "table-header",
        "logo-orange",
    }
    cards: list[dict[str, Any]] = []
    names = [name for name, _ in token_items(tokens, "color")]
    for start in range(0, len(names), 4):
        card_row: list[dict[str, Any]] = []
        for name in names[start : start + 4]:
            label_color = (
                "$color-primary-active" if name in dark_text else "$color-surface"
            )
            role, classification, usage = COLOR_ROLES[name]
            card = frame(
                f"color-card-{name}",
                name,
                [
                    text(
                        f"color-name-{name}",
                        name,
                        size=14,
                        weight=700,
                        color=label_color,
                    ),
                    text(
                        f"color-hex-{name}",
                        token_hex(tokens, name).upper(),
                        size=12,
                        color=label_color,
                    ),
                    text(
                        f"color-card-{name}-role",
                        f"Role · {role}",
                        size=9,
                        color=label_color,
                    ),
                    text(
                        f"color-card-{name}-classification",
                        f"Class · {classification}",
                        size=9,
                        color=label_color,
                    ),
                    text(
                        f"color-card-{name}-usage",
                        f"Use · {usage}",
                        size=9,
                        color=label_color,
                    ),
                ],
                gap=4,
                padding=12,
                width="fill_container",
                height=176,
                fill=f"$color-{name}",
                corner_radius="$radius-sm",
            )
            card["metadata"] = {
                "role": role,
                "classification": classification,
                "usage": usage,
            }
            card_row.append(card)
        cards.append(
            row(f"color-row-{start // 4}", f"Color row {start // 4 + 1}", card_row)
        )
    return section(
        "colors",
        "Color tokens",
        "All 20 normative colors, with observed, normalized and accessibility roles kept distinct",
        cards,
        index=index,
    )


def contrast_board(index: int) -> dict[str, Any]:
    cards = []
    for node_id, title, ratio, passes, background, foreground in CONTRAST_PAIRS:
        cards.append(
            frame(
                f"contrast-{node_id}",
                title,
                [
                    text(
                        f"contrast-{node_id}-sample",
                        "Readable sample Aa",
                        size=20,
                        weight=700,
                        color=foreground,
                    ),
                    text(
                        f"contrast-{node_id}-ratio",
                        f"{ratio} · {'AA normal text' if passes else 'FAIL normal text'}",
                        size=14,
                        weight=700,
                        color=foreground,
                    ),
                    text(
                        f"contrast-{node_id}-rule",
                        "Use with a text/icon cue; color is never the sole status signal."
                        if passes
                        else "Decorative/large emphasis only; use text-on-accent for normal copy.",
                        size=11,
                        color=foreground,
                    ),
                ],
                gap=12,
                padding=22,
                width="fill_container",
                height=210,
                fill=background,
                corner_radius="$radius-sm",
            )
        )
    rows = [
        row(
            f"contrast-row-{start // 2}",
            f"Contrast row {start // 2 + 1}",
            cards[start : start + 2],
        )
        for start in range(0, len(cards), 2)
    ]
    return section(
        "contrast",
        "Contrast and color accessibility",
        "Eight normative text pairs; borders require non-text contrast or an additional focus indicator",
        rows,
        index=index,
    )


def typography_board(tokens: dict[str, Any], index: int) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for name, token in token_items(tokens, "typography"):
        value = token["$value"]
        size = round(float(value["fontSize"]["value"]) * 16)
        tracking_rem = float(value["letterSpacing"]["value"])
        letter_spacing = tracking_rem * 16
        tracking = f"{letter_spacing / size:.2f}em"
        rows.append(
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
                        line_height=float(value["lineHeight"]),
                        letter_spacing=letter_spacing,
                    ),
                    text(
                        f"type-row-{name}-metrics",
                        f"{name} · {value['fontFamily']} · {size}px · weight {value['fontWeight']} · line {value['lineHeight']} · tracking {tracking}",
                        size=12,
                        color="$color-text-muted",
                    ),
                ],
                gap=5,
                padding=[12, 0],
                fill="#00000000",
                corner_radius=0,
            )
        )
    return section(
        "typography",
        "Typography roles",
        "All 10 roles with family, size, weight, line height and tracking; display and operational roles remain distinct",
        rows,
        index=index,
    )


def localization_board(index: int) -> dict[str, Any]:
    specimens = [
        frame(
            "type-sample-en",
            "English display",
            [
                text(
                    "type-sample-en-copy",
                    "Infrastructure with clarity",
                    size=38,
                    weight=700,
                    family="Pragati Narrow",
                ),
                text(
                    "type-sample-en-rule",
                    "Pragati Narrow is selective display emphasis, not general product UI.",
                    size=12,
                    color="$color-text-muted",
                ),
            ],
            padding=22,
            height=185,
            fill="$color-surface-subtle",
        ),
        frame(
            "type-sample-tc",
            "繁體中文 specimen",
            [
                text(
                    "type-sample-tc-copy",
                    "清晰可靠的基建管理",
                    size=30,
                    weight=700,
                    family="Noto Sans TC",
                ),
                text(
                    "type-sample-tc-rule",
                    "Use Noto Sans TC, then Microsoft JhengHei; never force Pragati Narrow onto Chinese glyphs.",
                    size=12,
                    color="$color-text-muted",
                ),
            ],
            padding=22,
            height=185,
            fill="$color-surface-subtle",
        ),
        frame(
            "type-sample-long",
            "Long-copy and expansion stress",
            [
                text(
                    "type-sample-long-copy",
                    "Project administration and compliance status · 項目管理及合規狀態 · 项目管理及合规状态",
                    size=18,
                    line_height=1.55,
                ),
                text(
                    "type-sample-long-rule",
                    "Allow wrapping without changing hierarchy; essential labels stay ≥14px and body copy targets 16px.",
                    size=12,
                    color="$color-text-muted",
                ),
            ],
            padding=22,
            height=185,
            fill="$color-table-header",
        ),
    ]
    rules = [
        (
            "type-rule-ui",
            "UI/body/data",
            "Roboto 400+ for controls, tables and operational copy.",
        ),
        (
            "type-rule-cjk",
            "Chinese fallback",
            "Verified CJK sans stack; test TC and SC content.",
        ),
        (
            "type-rule-wico",
            "Legacy wico",
            "Documentary source evidence only; never use in new products.",
        ),
        (
            "type-rule-license",
            "Font licensing",
            "Use upstream OFL-1.1 sources; hosted files do not grant redistribution rights.",
        ),
    ]
    return section(
        "localization-type",
        "Localization and type rules",
        "English, Traditional Chinese, Simplified Chinese and long-copy behavior share the same hierarchy",
        [
            *specimens,
            row(
                "type-rule-row",
                "Type governance",
                [
                    frame(
                        node_id,
                        title,
                        [text(f"{node_id}-copy", copy, size=11)],
                        padding=14,
                        height=120,
                        fill="$color-surface-muted",
                    )
                    for node_id, title, copy in rules
                ],
            ),
        ],
        index=index,
    )


def layout_board(tokens: dict[str, Any], index: int) -> dict[str, Any]:
    spacing_rows: list[dict[str, Any]] = []
    for name, token in token_items(tokens, "spacing"):
        px = int(token["$value"]["value"])
        spacing_rows.append(
            frame(
                f"space-row-{name}",
                name,
                [
                    text(
                        f"space-label-{name}",
                        f"{name} · {px}px",
                        size=12,
                        weight=700,
                        width=90,
                    ),
                    rectangle(
                        f"space-bar-{name}",
                        f"{name} spacing bar",
                        width=px * 4,
                        height=14,
                        fill="$color-accent",
                        corner_radius="$radius-sm",
                    ),
                ],
                layout="horizontal",
                gap=14,
                padding=5,
                fill="#00000000",
                corner_radius=0,
                alignItems="center",
            )
        )
    spacing_columns = [
        frame(
            "spacing-column-a",
            "Spacing 2xs–lg",
            spacing_rows[:5],
            gap=4,
            padding=14,
            width="fill_container",
            fill="$color-surface-subtle",
        ),
        frame(
            "spacing-column-b",
            "Spacing xl–5xl",
            spacing_rows[5:],
            gap=4,
            padding=14,
            width="fill_container",
            fill="$color-surface-subtle",
        ),
    ]
    radius_cards: list[dict[str, Any]] = []
    for name, token in token_items(tokens, "rounded"):
        px = int(token["$value"]["value"])
        radius_cards.append(
            frame(
                f"radius-{name}",
                name,
                [text(f"radius-label-{name}", f"{name} · {px}px", size=13, weight=700)],
                padding=14,
                width="fill_container",
                height=72,
                fill="$color-surface-muted",
                corner_radius=f"$radius-{name}",
            )
        )
    breakpoints = [
        ("compact", "370"),
        ("sm", "576"),
        ("md", "768"),
        ("lg", "992"),
        ("xl", "1200"),
        ("2xl", "1600"),
    ]
    breakpoint_cards = [
        frame(
            f"breakpoint-{name}",
            name,
            [
                text(
                    f"breakpoint-{name}-label",
                    f"{name}\n{value}px",
                    size=12,
                    weight=700,
                )
            ],
            padding=10,
            width="fill_container",
            height=62,
            fill="$color-table-header",
        )
        for name, value in breakpoints
    ]
    containers = [("sm", 540), ("md", 720), ("lg", 960), ("xl", 1140), ("2xl", 1570)]
    container_cards = [
        frame(
            f"container-{name}",
            name,
            [
                text(
                    f"container-{name}-label",
                    f"{name} · {value}px max",
                    size=11,
                    weight=700,
                )
            ],
            padding=10,
            width="fill_container",
            height=58,
            fill="$color-surface-muted",
        )
        for name, value in containers
    ]
    return section(
        "layout",
        "Layout and spacing",
        "4px rhythm, complete spacing/radius scales, source breakpoints and production composition rules",
        [
            row("spacing-columns", "Complete spacing scale", spacing_columns),
            row("radius-row", "Radius tokens", radius_cards),
            row("breakpoint-row-a", "Breakpoints compact–md", breakpoint_cards[:3]),
            row("breakpoint-row-b", "Breakpoints lg–2xl", breakpoint_cards[3:]),
            row("container-row", "Container maximums", container_cards),
            frame(
                "layout-composition",
                "Admin and CMS composition",
                [
                    text(
                        "layout-composition-title",
                        "Admin/CMS composition",
                        size=16,
                        weight=700,
                    ),
                    text(
                        "layout-composition-copy",
                        "Stable shell · title/action/status above fold · adjacent filters · 44px controls · responsive tables retain critical meaning · English/繁體中文 hierarchy",
                        size=13,
                    ),
                ],
                gap=8,
                padding=18,
                fill="$color-surface-muted",
            ),
        ],
        index=index,
    )


def depth_board(index: int) -> dict[str, Any]:
    elevation_cards = [
        frame(
            "elevation-none",
            "None / border first",
            [
                text(
                    "elevation-none-copy",
                    "none · 1px border before shadow",
                    size=14,
                    weight=700,
                )
            ],
            padding=20,
            width="fill_container",
            height=120,
            stroke="$color-border",
            strokeWidth=1,
        ),
        frame(
            "elevation-low",
            "Low elevation",
            [
                text(
                    "elevation-low-copy",
                    "0 4px 12px rgba(0,0,0,.10)\nNormalized, not observed token",
                    size=13,
                    weight=700,
                )
            ],
            padding=20,
            width="fill_container",
            height=120,
            effect={
                "type": "shadow",
                "shadowType": "outer",
                "offset": {"x": 0, "y": 4},
                "blur": 12,
                "spread": 0,
                "color": "#0000001a",
            },
        ),
    ]
    motion_cards = [
        ("duration-fast", "150ms", "Fast control feedback"),
        ("duration-standard", "200ms", "Standard product transition"),
        ("duration-brand", "600ms", "Non-blocking brand motion"),
        ("easing-standard", "ease-out", "Standard easing"),
        ("easing-brand", "cubic-bezier(.22,.61,.36,1)", "Brand easing"),
    ]
    motion_nodes = [
        frame(
            f"motion-{name}",
            name,
            [
                text(
                    f"motion-{name}-time",
                    duration,
                    size=18,
                    weight=700,
                    color="$color-primary",
                ),
                text(f"motion-{name}-copy", copy, size=11, color="$color-text-muted"),
            ],
            padding=14,
            width="fill_container",
            height=92,
            fill="$color-surface-subtle",
        )
        for name, duration, copy in motion_cards
    ]
    shape_nodes = [
        frame(
            f"shape-{name}",
            label,
            [text(f"shape-{name}-copy", copy, size=12, weight=700)],
            padding=16,
            width="fill_container",
            height=100,
            fill="$color-surface-muted",
            corner_radius=radius,
        )
        for name, label, copy, radius in [
            ("square", "Square", "Rails · panels · data", "$radius-none"),
            ("compact", "Compact", "Embedded elements", "$radius-sm"),
            ("control", "Control", "Fields · cards · dialogs", "$radius-md"),
            ("pill", "Pill", "Status badges only", "$radius-pill"),
        ]
    ]
    return section(
        "depth-shape-motion",
        "Elevation, motion and shapes",
        "Restrained depth, square-first geometry and motion that respects reduced-motion",
        [
            text("elevation-heading", "Elevation", size=20, weight=700),
            row("elevation-row", "Elevation samples", elevation_cards),
            text("motion-heading", "Motion", size=20, weight=700),
            row("motion-row", "Motion durations", motion_nodes),
            frame(
                "motion-reduced",
                "Reduced motion",
                [
                    text(
                        "motion-reduced-copy",
                        "Remove non-essential movement when prefers-reduced-motion is active.",
                        size=13,
                    )
                ],
                padding=16,
                fill="$color-table-header",
            ),
            text("shape-heading", "Shapes", size=20, weight=700),
            row("shape-row", "Shape language", shape_nodes),
            text(
                "shape-dont",
                "Do not introduce consumer-style 12–24px rounding, glow or glassmorphism.",
                size=13,
                color="$color-danger",
            ),
        ],
        index=index,
    )


def visual_card(
    name: str, component: dict[str, Any], evidence: dict[str, Any]
) -> dict[str, Any]:
    background = color_name(component.get("backgroundColor"))
    foreground = color_name(component.get("textColor"), "text")
    classification = evidence["classification"]
    values = " · ".join(
        f"{key}: {str(value).replace('{', '').replace('}', '')}"
        for key, value in component.items()
    )
    shape = (
        component.get("rounded", "{rounded.none}").strip("{}").removeprefix("rounded.")
    )
    card = frame(
        f"visual-{name}",
        name,
        [
            text(
                f"visual-{name}-title",
                name.replace("-", " ").title(),
                size=12,
                weight=700,
            ),
            frame(
                f"visual-{name}-preview",
                f"{name} preview",
                [
                    text(
                        f"visual-{name}-sample",
                        "Aa" if "swatch" in name else "Component sample",
                        size=12,
                        weight=700,
                        color=f"$color-{foreground}",
                    )
                ],
                padding=10,
                width="fill_container",
                height=54,
                fill=f"$color-{background}",
                corner_radius=f"$radius-{shape}",
                stroke="$color-border" if background == "surface" else None,
                strokeWidth=1 if background == "surface" else 0,
                alignItems="center",
            ),
            text(
                f"visual-{name}-classification",
                classification,
                size=10,
                color="$color-text-muted",
            ),
            text(
                f"visual-{name}-values",
                values,
                size=7,
                color="$color-text-muted",
            ),
        ],
        gap=8,
        padding=12,
        width=260,
        height=210,
        fill="$color-surface-subtle",
        stroke="$color-border",
        strokeWidth=1,
    )
    card["metadata"] = {
        "contractType": "visual",
        "contractName": name,
        "classification": classification,
        "component": component,
        "evidence": evidence,
    }
    return card


def visual_board(
    name: str,
    component_names: list[str],
    components: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    cards = [
        visual_card(
            component_name,
            components["components"][component_name],
            components["visual_component_evidence"][component_name],
        )
        for component_name in component_names
    ]
    rows = [
        row(
            f"visual-row-{index}-{start // 4}",
            f"Visual row {start // 4 + 1}",
            cards[start : start + 4],
        )
        for start in range(0, len(cards), 4)
    ]
    return section(
        f"visual-board-{index}",
        name,
        f"Complete visual records {len(component_names)} · values remain generated from DESIGN.md",
        rows,
        index=index,
    )


def behavior_card(
    name: str, contract: dict[str, Any], coverage: dict[str, Any]
) -> dict[str, Any]:
    evidence = contract["evidence"]
    mappings = list(coverage["stateMappings"].values())
    mapped = sum(item["status"] == "mapped" for item in mappings)
    behavior_only = len(mappings) - mapped
    card = frame(
        f"behavior-{name}",
        name,
        [
            text(
                f"behavior-{name}-title",
                name.replace("-", " ").title(),
                size=15,
                weight=700,
            ),
            frame(
                f"behavior-{name}-preview",
                f"{name} contract-only notice",
                [
                    text(
                        f"behavior-{name}-preview-copy",
                        "CONTRACT ONLY · NOT A SOURCE VISUAL\nSee Source component library boards for evidence-derived editable specimens.",
                        size=9,
                        weight=700,
                        color="$color-danger",
                    )
                ],
                padding=8,
                width="fill_container",
                height=40,
                fill="$color-surface",
                corner_radius="$radius-none",
                alignItems="center",
                stroke="$color-danger",
                strokeWidth=1,
            ),
            text(
                f"behavior-{name}-variants",
                f"Variants · {', '.join(contract['variants'])}",
                size=8,
            ),
            text(
                f"behavior-{name}-states",
                f"States · {', '.join(contract['states'])}",
                size=8,
            ),
            text(
                f"behavior-{name}-requirements",
                f"Requirements · {', '.join(contract['requirements'])}",
                size=8,
            ),
            text(
                f"behavior-{name}-coverage",
                f"Coverage · {mapped} mapped · {behavior_only} behavior-only",
                size=8,
                weight=700,
            ),
            text(
                f"behavior-{name}-evidence",
                f"Evidence · {evidence['classification']} · {evidence['pageLocations'][0]}",
                size=8,
                color="$color-text-muted",
            ),
        ],
        gap=4,
        padding=10,
        width=350,
        height=278,
        fill="$color-surface-subtle",
        stroke="$color-border",
        strokeWidth=1,
    )
    card["metadata"] = {
        "contractType": "behavior",
        "contractName": name,
        "classification": evidence["classification"],
        "variants": contract["variants"],
        "states": contract["states"],
        "requirements": contract["requirements"],
        "implementationCoverage": coverage,
    }
    return card


def behavior_board(
    board_id: str,
    name: str,
    component_names: list[str],
    contracts: dict[str, Any],
    coverage: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    cards = [
        behavior_card(
            component_name, contracts[component_name], coverage[component_name]
        )
        for component_name in component_names
    ]
    rows = [
        row(
            f"{board_id}-row-{start // 3}",
            f"Behavior row {start // 3 + 1}",
            cards[start : start + 3],
        )
        for start in range(0, len(cards), 3)
    ]
    return section(
        board_id,
        name,
        f"{len(component_names)} complete contracts · mini visual, variants, states, requirements and evidence",
        rows,
        index=index,
    )


def implementation_matrix_board(
    components: dict[str, Any], index: int
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for name, coverage in components["implementation_coverage"].items():
        cells = []
        mappings = coverage["stateMappings"]
        for pair, mapping in mappings.items():
            variant, state = pair.split(".", 1)
            cell = rectangle(
                f"coverage-cell-{name}-{variant}-{state}",
                f"{name} · {variant} · {state} · {mapping['status']}",
                width=8,
                height=8,
                fill="$color-primary"
                if mapping["status"] == "mapped"
                else "$color-border",
                corner_radius=2,
            )
            cell["metadata"] = mapping
            cells.append(cell)
        mapped = sum(mapping["status"] == "mapped" for mapping in mappings.values())
        matrix = frame(
            f"coverage-cells-{name}",
            f"{name} state cells",
            cells,
            layout="horizontal",
            gap=3,
            padding=0,
            width="fill_container",
            height=10,
            fill="#00000000",
            corner_radius=0,
        )
        rows.append(
            frame(
                f"coverage-row-{name}",
                name,
                [
                    text(
                        f"coverage-row-{name}-name", name, size=9, weight=700, width=150
                    ),
                    text(
                        f"coverage-row-{name}-summary",
                        f"{mapped} mapped · {len(mappings) - mapped} behavior-only",
                        size=8,
                        width=170,
                    ),
                    matrix,
                ],
                layout="horizontal",
                gap=12,
                padding=[4, 8],
                width="fill_container",
                height=25,
                fill="$color-surface-subtle"
                if len(rows) % 2 == 0
                else "$color-surface",
                corner_radius=0,
                alignItems="center",
            )
        )
    return section(
        "implementation-matrix",
        "Variant and state implementation",
        "All 345 variant × state cells · green = mapped implementation · grey = behavior-only contract",
        [
            row(
                "implementation-legend",
                "Implementation legend",
                [
                    frame(
                        "implementation-mapped",
                        "Mapped",
                        [
                            text(
                                "implementation-mapped-copy",
                                "■ 48 mapped",
                                size=12,
                                weight=700,
                                color="$color-primary",
                            )
                        ],
                        padding=10,
                        fill="$color-surface-subtle",
                    ),
                    frame(
                        "implementation-behavior-only",
                        "Behavior only",
                        [
                            text(
                                "implementation-behavior-only-copy",
                                "■ 297 behavior-only",
                                size=12,
                                weight=700,
                                color="$color-text-muted",
                            )
                        ],
                        padding=10,
                        fill="$color-surface-subtle",
                    ),
                ],
            ),
            frame(
                "implementation-rows",
                "All implementation rows",
                rows,
                gap=2,
                padding=0,
                width="fill_container",
                fill="#00000000",
                corner_radius=0,
            ),
        ],
        index=index,
    )


def accessibility_assets_board(
    components: dict[str, Any], index: int
) -> dict[str, Any]:
    requirements = [
        (component, requirement)
        for component, contract in components["behavior_contracts"].items()
        for requirement in contract["requirements"]
    ]
    column_count = 5
    per_column = (len(requirements) + column_count - 1) // column_count
    columns = []
    for column_index in range(column_count):
        items = requirements[
            column_index * per_column : (column_index + 1) * per_column
        ]
        columns.append(
            frame(
                f"requirement-column-{column_index}",
                f"Requirement column {column_index + 1}",
                [
                    text(
                        f"requirement-{component}-{requirement}",
                        f"{component} · {requirement}",
                        size=8,
                    )
                    for component, requirement in items
                ],
                gap=3,
                padding=10,
                width="fill_container",
                fill="$color-surface-subtle",
            )
        )
    asset_rules = [
        (
            "assets-svg-icons",
            "Approved SVG icons",
            "Use an approved, licensed SVG library with accessible names.",
        ),
        (
            "assets-icon-font",
            "Legacy wico boundary",
            "Source evidence only; do not import the public icon font.",
        ),
        (
            "assets-licensing",
            "Licensing",
            "Pin asset/font licences and retain upstream notices.",
        ),
        (
            "assets-imagery",
            "Imagery",
            "Use approved real project imagery; never place essential text on untested images.",
        ),
    ]
    return section(
        "accessibility-assets",
        "Accessibility, icons and assets",
        f"All {len(requirements)} behavior requirements plus explicit icon, font, image and licensing governance",
        [
            row("requirement-columns", "Complete requirement register", columns, gap=8),
            row(
                "asset-rule-row",
                "Asset governance",
                [
                    frame(
                        node_id,
                        title,
                        [text(f"{node_id}-copy", copy, size=10)],
                        padding=14,
                        height=130,
                        fill="$color-table-header",
                    )
                    for node_id, title, copy in asset_rules
                ],
            ),
        ],
        index=index,
    )


def responsive_preview(
    node_id: str, label: str, width: int, mode: str
) -> dict[str, Any]:
    compact = mode == "mobile"
    body = [
        frame(
            f"{node_id}-header",
            "Application header",
            [
                text(
                    f"{node_id}-brand",
                    "Company Admin",
                    size=10,
                    weight=700,
                    color="$color-surface",
                )
            ],
            layout="horizontal",
            padding=10,
            width="fill_container",
            height=42,
            fill="$color-primary-dark",
            corner_radius=0,
        ),
        frame(
            f"{node_id}-toolbar",
            "Title and action",
            [
                text(f"{node_id}-title-copy", "Projects", size=13, weight=700),
                text(
                    f"{node_id}-action",
                    "+ Create",
                    size=10,
                    weight=700,
                    color="$color-surface",
                ),
            ],
            layout="horizontal",
            padding=10,
            width="fill_container",
            height=48,
            fill="$color-surface-subtle",
            corner_radius=0,
        ),
        frame(
            f"{node_id}-data",
            "Responsive data surface",
            [
                text(
                    f"{node_id}-data-copy",
                    "Project A\nStatus · Active\nOwner · Operations"
                    if compact
                    else "PROJECT       STATUS       OWNER\nProject A     Active       Operations\nProject B     Review       Engineering",
                    size=9,
                )
            ],
            padding=12,
            width="fill_container",
            height=150 if compact else 116,
            fill="$color-surface",
            stroke="$color-border",
            strokeWidth=1,
        ),
    ]
    return frame(
        node_id,
        label,
        [
            text(f"{node_id}-label", label, size=14, weight=700),
            text(f"{node_id}-mode", mode, size=10, color="$color-text-muted"),
            *body,
        ],
        gap=8,
        padding=14,
        width=width,
        height=470,
        fill="$color-surface-muted",
        corner_radius="$radius-sm",
    )


def responsive_board(index: int) -> dict[str, Any]:
    return section(
        "responsive",
        "Responsive compositions",
        "Actual admin/CMS composition at three governed viewports; critical data remains visible",
        [
            row(
                "responsive-row",
                "Desktop tablet mobile",
                [
                    responsive_preview(
                        "responsive-desktop", "Desktop · 1440", 500, "desktop"
                    ),
                    responsive_preview(
                        "responsive-tablet", "Tablet · 768", 310, "tablet"
                    ),
                    responsive_preview(
                        "responsive-mobile", "Mobile · 390", 220, "mobile"
                    ),
                ],
                gap=14,
            ),
            frame(
                "responsive-rules",
                "Responsive rules",
                [
                    text(
                        "responsive-rules-title",
                        "Preserve meaning, not desktop geometry",
                        size=18,
                        weight=700,
                    ),
                    text(
                        "responsive-rules-copy",
                        "Desktop uses workspace; tablet reduces columns; mobile stacks labelled rows. Filters stay adjacent, controls remain ≥44px, critical columns are never silently hidden, and English/繁體中文 expansion is allowed.",
                        size=14,
                    ),
                ],
                padding=20,
                fill="$color-table-header",
            ),
        ],
        index=index,
    )


def page_patterns_board(index: int) -> dict[str, Any]:
    cards = [
        frame(
            f"page-pattern-{node_id}",
            title,
            [
                text(f"page-pattern-{node_id}-title", title, size=16, weight=700),
                text(f"page-pattern-{node_id}-copy", copy, size=11),
                text(
                    f"page-pattern-{node_id}-boundary",
                    "Observed browser-profile family · adapt behavior; do not copy public composition.",
                    size=9,
                    color="$color-text-muted",
                ),
            ],
            gap=9,
            padding=18,
            width=350,
            height=190,
            fill="$color-surface-subtle",
            stroke="$color-border",
            strokeWidth=1,
        )
        for node_id, title, copy in PAGE_PATTERNS
    ]
    return section(
        "page-patterns",
        "Page patterns and adaptation",
        "Eleven summarized browser-profile families; these are evidence groupings, not an authored-template count",
        [
            row(
                f"page-pattern-row-{start // 3}",
                f"Page pattern row {start // 3 + 1}",
                cards[start : start + 3],
            )
            for start in range(0, len(cards), 3)
        ],
        index=index,
    )


def evidence_board(index: int) -> dict[str, Any]:
    cards = [
        (
            "evidence-observed",
            "Observed source evidence",
            "Public CSS declarations, exact live URL/location pairs and visible computed samples are retained in the evidence register.",
            "$color-primary",
            "$color-surface",
        ),
        (
            "evidence-cross-page",
            "Cross-page observed pattern",
            "Repeated family behavior is backed by concrete profile URLs and locations; repetition does not make it an official component.",
            "$color-primary-dark",
            "$color-surface",
        ),
        (
            "evidence-normalized",
            "Normalized product mapping",
            "Spacing, 44px controls, semantic roles and behavior-only contracts are product decisions—not official source tokens.",
            "$color-surface-subtle",
            "$color-text",
        ),
        (
            "evidence-accessibility",
            "Accessibility correction",
            "accent-accessible #B15315 and text-on-accent #001C19 are scaffold corrections. Orange/white is not normal-text AA.",
            "$color-accent-accessible",
            "$color-surface",
        ),
        (
            "evidence-not-observed",
            "Not observed",
            "CSS-only declarations and behavior-only states remain pageLocation ‘not observed’; they are never presented as rendered live states.",
            "$color-table-header",
            "$color-text",
        ),
    ]
    nodes = [
        frame(
            node_id,
            title,
            [
                text(f"{node_id}-title", title, size=20, weight=700, color=foreground),
                text(f"{node_id}-copy", copy, size=14, color=foreground),
            ],
            gap=10,
            padding=24,
            height=190,
            fill=background,
            corner_radius="$radius-none",
        )
        for node_id, title, copy, background, foreground in cards
    ]
    return section(
        "evidence",
        "Evidence and provenance",
        "Every visual claim stays classified; DESIGN.md remains the only normative source",
        [
            *nodes,
            text(
                "evidence-links",
                "Normative: DESIGN.md · Generated: design-system/ · Human register: docs/design-system/source-evidence.md",
                size=13,
                color="$color-text-muted",
            ),
        ],
        index=index,
    )


def coverage_board(components: dict[str, Any], index: int) -> dict[str, Any]:
    statuses = [
        state["status"]
        for contract in components["implementation_coverage"].values()
        for state in contract["stateMappings"].values()
    ]
    metadata = {
        "behaviorContracts": len(components["behavior_contracts"]),
        "visualContracts": len(components["components"]),
        "variantStateMappings": len(statuses),
        "mapped": statuses.count("mapped"),
        "behaviorOnly": statuses.count("behavior-only"),
    }
    cards = [
        (
            "coverage-sitemap",
            "Discovery",
            "10,666 unique sitemap URLs",
            "Complete sitemap discovery; not individual browser rendering.",
        ),
        (
            "coverage-http",
            "Deterministic HTTP coverage",
            "559/559 locale-specific routes",
            "EN 188 · TC 175 · SC 196 · coverage units, not authored templates.",
        ),
        (
            "coverage-browser",
            "Rendered evidence",
            "43 profiles × 3 viewports = 129",
            "1,022 visible default samples · 255 successful state samples · 0 failures.",
        ),
        (
            "coverage-implementation",
            "Implementation mapping",
            f"{metadata['mapped']} mapped · {metadata['behaviorOnly']} behavior-only",
            f"{metadata['variantStateMappings']} variant-state mappings across 31 behavior contracts; behavior-only is not claimed as implemented UI.",
        ),
    ]
    board = section(
        "coverage",
        "Coverage and limitations",
        "Discovery, HTTP, browser evidence and implementation coverage are separate layers",
        [
            frame(
                node_id,
                title,
                [
                    text(f"{node_id}-title", title, size=18, weight=700),
                    text(
                        f"{node_id}-metric",
                        metric,
                        size=26,
                        weight=700,
                        color="$color-primary",
                    ),
                    text(f"{node_id}-copy", copy, size=13, color="$color-text-muted"),
                ],
                gap=9,
                padding=24,
                height=205,
                fill="$color-surface-subtle",
                stroke="$color-border",
                strokeWidth=1,
            )
            for node_id, title, metric, copy in cards
        ],
        index=index,
    )
    board["metadata"] = metadata
    return board


def guidance_board(index: int) -> dict[str, Any]:
    do_items = [
        "Use deep green structurally and orange as restrained accent.",
        "Build from normative tokens/contracts, not hardcoded colors.",
        "Use real project imagery only when it improves understanding.",
        "Keep operational products clear, dense and predictable.",
        "Validate text, focus and non-text contrast to WCAG AA.",
        "Support English/繁體中文 without hierarchy changes.",
        "Preserve loading, empty, error, success and action states.",
        "Re-run the evidence audit when source CSS hashes change.",
    ]
    dont_items = [
        "Do not call this an official corporate brand manual.",
        "Do not copy the public hero, carousel or mega-menu into admin.",
        "Do not place normal white text on raw #E6762D.",
        "Do not use logo colors as generic product statuses.",
        "Do not introduce pink, neon, glass or unrelated gradients.",
        "Do not use giant rounded cards or consumer-app softness.",
        "Do not put essential text on untested project imagery.",
        "Do not import public CSS, logos, icon fonts or content.",
    ]
    return section(
        "guidance",
        "Do and don't",
        "Operational guardrails from the normative specification",
        [
            frame(
                "guidance-do",
                "Do",
                [
                    text(
                        "guidance-do-title",
                        "DO",
                        size=24,
                        weight=700,
                        color="$color-surface",
                    ),
                    *[
                        text(
                            f"guidance-do-{i}",
                            f"+ {item}",
                            size=13,
                            color="$color-surface",
                        )
                        for i, item in enumerate(do_items)
                    ],
                ],
                gap=11,
                padding=24,
                height=460,
                fill="$color-primary",
                corner_radius="$radius-none",
            ),
            frame(
                "guidance-dont",
                "Don't",
                [
                    text(
                        "guidance-dont-title",
                        "DON'T",
                        size=24,
                        weight=700,
                        color="$color-surface",
                    ),
                    *[
                        text(
                            f"guidance-dont-{i}",
                            f"− {item}",
                            size=13,
                            color="$color-surface",
                        )
                        for i, item in enumerate(dont_items)
                    ],
                ],
                gap=11,
                padding=24,
                height=460,
                fill="$color-danger",
                corner_radius="$radius-none",
            ),
        ],
        index=index,
    )


def cover_board(index: int, input_sha256: dict[str, str]) -> dict[str, Any]:
    cover = section(
        "cover",
        "Cover",
        "Complete visual derivative of DESIGN.md · generated, not a second source of truth",
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
                height=390,
                fill="$color-primary-dark",
                corner_radius="$radius-none",
            ),
            frame(
                "cover-catalogue",
                "Catalogue coverage",
                [
                    text(
                        "cover-catalogue-title",
                        "35 governed boards",
                        size=24,
                        weight=700,
                    ),
                    text(
                        "cover-catalogue-copy",
                        "52 public component families (40 live · 9 CSS-reference · 3 not observed) · 24 detailed interactive specimens · 31 visual contracts · 31 behavior contracts",
                        size=16,
                    ),
                ],
                padding=28,
                fill="$color-table-header",
            ),
            frame(
                "cover-facts",
                "Audit coverage",
                [
                    text(
                        "cover-fact-a",
                        "10,666 URLs discovered · 559/559 route units",
                        size=18,
                        weight=700,
                    ),
                    text(
                        "cover-fact-b",
                        "129 profile/viewport records · 1,022 default + 255 state samples",
                        size=16,
                    ),
                    text(
                        "cover-fact-c",
                        "Observed ≠ normalized ≠ accessibility correction",
                        size=16,
                    ),
                ],
                gap=12,
                padding=24,
                fill="$color-surface-subtle",
            ),
        ],
        index=index,
    )
    cover["metadata"] = {
        "type": "design-system-visualization",
        "normativeSource": "DESIGN.md",
        "generatedFrom": [
            "DESIGN.md",
            "design-system/tokens.json",
            "design-system/components.json",
            "design-system/source-component-specimens.json",
            "docs/design-system/evidence/source-evidence-index.json",
        ],
        "exporterVersion": 5,
        "auditDate": "2026-08-19",
        "validatedWith": "pen 0.3.3",
        "inputSha256": input_sha256,
    }
    return cover


def build_document(
    tokens: dict[str, Any],
    components: dict[str, Any],
    source_specimens: dict[str, Any],
    source_evidence_index: dict[str, Any],
    input_sha256: dict[str, str],
) -> dict[str, Any]:
    variables: dict[str, Any] = {
        f"color-{name}": {"type": "color", "value": token_hex(tokens, name)}
        for name, _ in token_items(tokens, "color")
    }
    variables.update(
        {
            f"spacing-{name}": {
                "type": "number",
                "value": token_px(tokens, "spacing", name),
            }
            for name, _ in token_items(tokens, "spacing")
        }
    )
    variables.update(
        {
            f"radius-{name}": {
                "type": "number",
                "value": token_px(tokens, "rounded", name),
            }
            for name, _ in token_items(tokens, "rounded")
        }
    )

    boards: list[dict[str, Any]] = [
        cover_board(0, input_sha256),
        color_board(tokens, 1),
        contrast_board(2),
        typography_board(tokens, 3),
        localization_board(4),
        layout_board(tokens, 5),
        depth_board(6),
    ]
    for index, (name, visual_names) in enumerate(VISUAL_GROUPS.items(), start=7):
        boards.append(visual_board(name, visual_names, components, index))
    behavior_start = len(boards)
    for offset, (name, behavior_names) in enumerate(BEHAVIOR_GROUPS.items()):
        board_id = [
            "behavior-actions-navigation",
            "behavior-forms-selection",
            "behavior-content-data",
            "behavior-feedback-system",
        ][offset]
        boards.append(
            behavior_board(
                board_id,
                name,
                behavior_names,
                components["behavior_contracts"],
                components["implementation_coverage"],
                behavior_start + offset,
            )
        )
    boards.extend(
        [
            implementation_matrix_board(components, 13),
            accessibility_assets_board(components, 14),
            responsive_board(15),
            page_patterns_board(16),
            evidence_board(17),
            coverage_board(components, 18),
            guidance_board(19),
        ]
    )
    boards.extend(
        source_component_boards(
            source_specimens,
            components["behavior_contracts"],
            len(boards),
        )
    )
    boards.extend(
        public_component_catalogue_boards(
            source_evidence_index["public_component_evidence"], len(boards)
        )
    )

    expected_visuals = set(components["components"])
    rendered_visuals = {name for names in VISUAL_GROUPS.values() for name in names}
    expected_behaviors = set(components["behavior_contracts"])
    rendered_behaviors = {name for names in BEHAVIOR_GROUPS.values() for name in names}
    if rendered_visuals != expected_visuals:
        raise ValueError(
            f"Visual contract grouping drift: {sorted(expected_visuals ^ rendered_visuals)}"
        )
    if rendered_behaviors != expected_behaviors:
        raise ValueError(
            f"Behavior contract grouping drift: {sorted(expected_behaviors ^ rendered_behaviors)}"
        )
    if len(boards) != 35:
        raise ValueError(f"Expected 35 boards, got {len(boards)}")

    return {"version": "2.17", "variables": variables, "children": boards}


def render() -> str:
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    components = json.loads(COMPONENTS_PATH.read_text(encoding="utf-8"))
    source_specimens = json.loads(SOURCE_SPECIMENS_PATH.read_text(encoding="utf-8"))
    source_evidence_index = json.loads(
        SOURCE_EVIDENCE_INDEX_PATH.read_text(encoding="utf-8")
    )
    input_sha256 = {
        "DESIGN.md": hashlib.sha256(DESIGN_PATH.read_bytes()).hexdigest(),
        "design-system/tokens.json": hashlib.sha256(
            TOKENS_PATH.read_bytes()
        ).hexdigest(),
        "design-system/components.json": hashlib.sha256(
            COMPONENTS_PATH.read_bytes()
        ).hexdigest(),
        "design-system/source-component-specimens.json": hashlib.sha256(
            SOURCE_SPECIMENS_PATH.read_bytes()
        ).hexdigest(),
        "docs/design-system/evidence/source-evidence-index.json": hashlib.sha256(
            SOURCE_EVIDENCE_INDEX_PATH.read_bytes()
        ).hexdigest(),
    }
    return (
        json.dumps(
            build_document(
                tokens,
                components,
                source_specimens,
                source_evidence_index,
                input_sha256,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export the complete pen.dev visual design-system catalogue"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated catalogue has drifted",
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
        print(f"Verified pen.dev catalogue: {OUTPUT_PATH.relative_to(ROOT)}")
        return 0
    OUTPUT_PATH.write_text(expected, encoding="utf-8")
    print(f"Generated pen.dev catalogue: {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
