from __future__ import annotations

import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
is_allowed_source_url = runpy.run_path(
    str(ROOT / "scripts" / "audit_aai_design_system.py")
)["is_allowed_source_url"]
EVIDENCE = ROOT / "docs" / "design-system" / "evidence"
EXPECTED_COLORS = {
    "primary": "#006a63",
    "primary-dark": "#003531",
    "primary-active": "#001c19",
    "accent": "#e6762d",
    "accent-accessible": "#b15315",
    "accent-selected": "#733208",
    "text": "#333333",
    "text-muted": "#6c757d",
    "surface": "#ffffff",
    "surface-subtle": "#f7f7f7",
    "surface-muted": "#ececec",
    "surface-disabled": "#eaeaea",
    "border": "#cecece",
    "table-header": "#fff2ea",
    "focus": "#006a63",
    "danger": "#dc3545",
    "success": "#006a63",
    "logo-orange": "#f7941d",
    "logo-olive": "#7b7a1b",
}
EXPECTED_LINE_HEIGHTS = {
    "display-lg": 1,
    "heading-xl": 1.1,
    "heading-lg": 1.2,
    "heading-md": 1.25,
    "heading-sm": 1.3,
    "body-lg": 1.55,
    "body-md": 1.5,
    "body-sm": 1.45,
    "label": 1.25,
    "caption": 1.35,
}
EXTENSION_KEY = "com.github.corgimomo2023.company-fullstack-scaffold"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contrast_ratio(foreground: str, background: str) -> float:
    def luminance(value: str) -> float:
        channels = [int(value[index : index + 2], 16) / 255 for index in (1, 3, 5)]
        linear = [
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
            for channel in channels
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

    lighter, darker = sorted(
        (luminance(foreground), luminance(background)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def test_public_audit_url_scope_uses_exact_origin_matching() -> None:
    assert is_allowed_source_url("https://www.asiaalliedgroup.com/css/projectbase.css")
    assert not is_allowed_source_url(
        "http://www.asiaalliedgroup.com/css/projectbase.css"
    )
    assert not is_allowed_source_url("https://asiaalliedgroup.com/css/projectbase.css")
    assert not is_allowed_source_url(
        "https://www.asiaalliedgroup.com.evil.example/projectbase.css"
    )
    assert not is_allowed_source_url(
        "https://evil.example/projectbase.css?from=asiaalliedgroup.com"
    )
    assert not is_allowed_source_url(
        "https://www.asiaalliedgroup.com@evil.example/projectbase.css"
    )


def test_sitemap_and_template_audit_is_complete_and_error_free() -> None:
    audit = load_json(EVIDENCE / "site-map-and-template-audit.json")
    scope = audit["scope"]

    assert scope["total_sitemap_entries"] == 10_669
    assert scope["total_unique_sitemap_urls"] == 10_666
    assert scope["representative_page_count"] == 100
    assert audit["validation"] == {
        "page_error_count": 0,
        "page_errors": [],
        "unexpected_stylesheet_count": 0,
        "missing_expected_stylesheet_count": 0,
    }

    expected_locale_counts = {
        "en": (3_771, 3_770),
        "tc": (2_879, 2_878),
        "sc": (4_019, 4_018),
    }
    for locale, (entries, unique) in expected_locale_counts.items():
        sitemap = scope["sitemaps"][locale]
        assert sitemap["url_count"] == entries
        assert sitemap["unique_url_count"] == unique
        assert sitemap["duplicate_count"] == 1
        assert not sitemap["invalid_scope_urls"]

    pages = audit["representative_pages"]
    assert len(pages) == 100
    assert all(page["status"] != "error" for page in pages)
    assert {page["locale"] for page in pages} == {"en", "tc", "sc"}
    assert sum(page["url"] != page["final_url"] for page in pages) == 15
    assert sum("pdf" in (page.get("content_type") or "").lower() for page in pages) == 3


def test_stylesheet_evidence_has_expected_hashes_and_brand_values() -> None:
    evidence = load_json(EVIDENCE / "css-token-evidence.json")
    assert "at most 3" in evidence["provenance"]["excerpt_policy"]
    stylesheets = {
        item["source_url"].rsplit("/", 1)[-1]: item for item in evidence["stylesheets"]
    }

    project = stylesheets["projectbase.css"]
    assert (
        project["sha256"]
        == "ff62bae815e73cb956e935b15bb4df7bec36e6c8013c38bd69a8bc7ab3f5dc94"
    )
    assert project["bytes"] == 454_544
    assert project["parsed_rule_count"] == 2_883
    assert project["colors"]["#E6762D"]["count"] == 60
    assert project["colors"]["#006A63"]["count"] == 32
    assert project["colors"]["#003531"]["count"] == 10
    assert project["media_queries"]["max-width: 767.98px"] == 112
    assert project["media_queries"]["max-width: 991.98px"] == 103
    assert all("src" not in face for face in project["font_faces"])
    assert all(len(item["evidence"]) <= 3 for item in project["colors"].values())
    assert all(
        len(item["top_values"]) <= 25 for item in project["property_values"].values()
    )

    print_css = stylesheets["print.css"]
    assert (
        print_css["sha256"]
        == "b99d6336f7da208f0d859a30cdbd0fb3e2cb1cff138732013a208751d9ae2e98"
    )
    assert print_css["bytes"] == 256_301


def test_generated_formats_share_the_normative_contract() -> None:
    tailwind = load_json(ROOT / "design-system" / "tailwind.theme.json")
    assert tailwind["theme"]["extend"]["colors"] == EXPECTED_COLORS
    for name, line_height in EXPECTED_LINE_HEIGHTS.items():
        assert tailwind["theme"]["extend"]["fontSize"][name][1]["lineHeight"] == str(
            line_height
        )

    dtcg = load_json(ROOT / "design-system" / "tokens.json")
    assert dtcg["$schema"] == "https://www.designtokens.org/schemas/2025.10/format.json"
    dtcg_colors = {
        name: token["$value"]["hex"]
        for name, token in dtcg["color"].items()
        if not name.startswith("$")
    }
    assert dtcg_colors == EXPECTED_COLORS
    for name, line_height in EXPECTED_LINE_HEIGHTS.items():
        value = dtcg["typography"][name]["$value"]
        assert value["lineHeight"] == line_height
        assert value["letterSpacing"]["unit"] in {"px", "rem"}

    components = load_json(ROOT / "design-system" / "components.json")
    extension_components = dtcg["$extensions"][EXTENSION_KEY]["componentContract"]
    assert len(extension_components) == 21
    assert components["components"] == extension_components

    theme_css = (ROOT / "design-system" / "theme.css").read_text(encoding="utf-8")
    css_colors = dict(re.findall(r"--color-([a-z0-9-]+):\s*(#[0-9a-f]{6});", theme_css))
    assert css_colors == EXPECTED_COLORS
    assert '--font-display-lg: "Pragati Narrow";' in theme_css
    assert '--font-body-md: "Roboto";' in theme_css
    assert '"Pragati Narrow, Roboto' not in theme_css
    for name, line_height in EXPECTED_LINE_HEIGHTS.items():
        assert f"--leading-{name}: {line_height};" in theme_css


def test_normative_color_pairs_meet_wcag_aa() -> None:
    required_normal_text_pairs = [
        ("#ffffff", EXPECTED_COLORS["primary"]),
        ("#ffffff", EXPECTED_COLORS["primary-dark"]),
        ("#ffffff", EXPECTED_COLORS["primary-active"]),
        ("#ffffff", EXPECTED_COLORS["accent-accessible"]),
        ("#ffffff", EXPECTED_COLORS["accent-selected"]),
        ("#ffffff", EXPECTED_COLORS["danger"]),
        (EXPECTED_COLORS["text"], EXPECTED_COLORS["surface"]),
        (EXPECTED_COLORS["text-muted"], EXPECTED_COLORS["surface"]),
        (EXPECTED_COLORS["text"], EXPECTED_COLORS["table-header"]),
    ]
    assert all(contrast_ratio(fg, bg) >= 4.5 for fg, bg in required_normal_text_pairs)
    assert contrast_ratio("#ffffff", EXPECTED_COLORS["accent"]) < 4.5


def test_design_documents_do_not_claim_official_brand_manual() -> None:
    design = (ROOT / "DESIGN.md").read_text(encoding="utf-8")
    source_audit = (ROOT / "docs" / "design-system" / "source-audit.md").read_text(
        encoding="utf-8"
    )
    inventory = (ROOT / "docs" / "design-system" / "component-inventory.md").read_text(
        encoding="utf-8"
    )

    assert "not an official corporate brand manual" in design
    assert "every content URL was individually fetched" in source_audit
    assert "does **not** claim" in source_audit
    assert "Selectors are evidence labels, not code to copy" in inventory
