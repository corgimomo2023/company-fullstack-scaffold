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
OUTPUT_PATH = ROOT / "design-system" / "asia-allied-design-system.pen"

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1240
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

PREVIEW_COPY = {
    "button": "Save changes",
    "icon-button": "＋  ⋯  ×",
    "link": "View project →",
    "tag-filter": "All   ESG   Projects",
    "pagination": "‹ Prev   1  [2]  3   Next ›",
    "tabs": "Overview   [Details]   Files",
    "navigation": "Dashboard   Projects   Reports",
    "breadcrumb": "Home / Projects / Detail",
    "dropdown-menu": "Actions  ▾   Edit · Export",
    "text-input": "Project name",
    "textarea": "Add operational notes…",
    "select": "Status: Active  ▾",
    "checkbox": "☑ Email updates   ☐ SMS",
    "radio": "● Internal   ○ External",
    "field": "Label · Control · Help text",
    "search": "⌕  Search projects",
    "card": "Project card · status · action",
    "media-card": "▧  Image · title · metadata",
    "metric-card": "Active projects   128  +12%",
    "table": "NAME        STATUS      OWNER",
    "accordion": "2025 development history  ＋",
    "carousel": "‹   Feature 02 / 04   ›   ‖",
    "timeline": "● 2001 ── ● 2012 ── ● 2025",
    "map": "HK ●     SG ●       AU ●",
    "file-download": "Annual report · PDF · 4.2 MB ↓",
    "status-badge": "Success   Warning   Error",
    "dialog": "Confirm action   Cancel | Continue",
    "alert": "Important operational message",
    "toast": "Changes saved successfully",
    "empty-state": "No projects yet · Create project",
    "loading-skeleton": "██████   █████████   ████",
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
                f"{name} mini visual",
                [
                    text(
                        f"behavior-{name}-preview-copy",
                        PREVIEW_COPY[name],
                        size=11,
                        weight=700,
                        color="$color-primary",
                    )
                ],
                padding=8,
                width="fill_container",
                height=40,
                fill="$color-table-header",
                corner_radius="$radius-sm",
                alignItems="center",
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
                        "20 governed boards",
                        size=24,
                        weight=700,
                    ),
                    text(
                        "cover-catalogue-copy",
                        "62 token evidence records · 31 visual contracts · 31 behavior contracts · 345 state cells · 101 requirements · responsive and page-pattern adaptation",
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
        ],
        "exporterVersion": 3,
        "auditDate": "2026-08-19",
        "validatedWith": "pen 0.3.3",
        "inputSha256": input_sha256,
    }
    return cover


def build_document(
    tokens: dict[str, Any],
    components: dict[str, Any],
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
    if len(boards) != 20:
        raise ValueError(f"Expected 20 boards, got {len(boards)}")

    return {"version": "2.17", "variables": variables, "children": boards}


def render() -> str:
    tokens = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    components = json.loads(COMPONENTS_PATH.read_text(encoding="utf-8"))
    input_sha256 = {
        "DESIGN.md": hashlib.sha256(DESIGN_PATH.read_bytes()).hexdigest(),
        "design-system/tokens.json": hashlib.sha256(
            TOKENS_PATH.read_bytes()
        ).hexdigest(),
        "design-system/components.json": hashlib.sha256(
            COMPONENTS_PATH.read_bytes()
        ).hexdigest(),
    }
    return (
        json.dumps(
            build_document(tokens, components, input_sha256),
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
