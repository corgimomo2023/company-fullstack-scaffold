from __future__ import annotations

import json
import re
import runpy
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT_HELPERS = runpy.run_path(str(ROOT / "scripts" / "audit_aai_design_system.py"))
is_allowed_source_url = AUDIT_HELPERS["is_allowed_source_url"]
normalized_route_signature = AUDIT_HELPERS["normalized_route_signature"]
fetch = AUDIT_HELPERS["fetch"]
select_representative_pages = AUDIT_HELPERS["select_representative_pages"]
SameOriginRedirectHandler = AUDIT_HELPERS["SameOriginRedirectHandler"]
EVIDENCE = ROOT / "docs" / "design-system" / "evidence"
EXPECTED_COLORS = {
    "primary": "#006a63",
    "primary-dark": "#003531",
    "primary-active": "#001c19",
    "accent": "#e6762d",
    "accent-accessible": "#b15315",
    "accent-selected": "#733208",
    "text-on-accent": "#001c19",
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


def test_public_audit_fetch_and_redirect_paths_fail_closed_outside_origin() -> None:
    with pytest.raises(ValueError, match="outside the audited HTTPS origin"):
        fetch("http://169.254.169.254/latest/meta-data", retries=1)

    handler = SameOriginRedirectHandler()
    request = urllib.request.Request("https://www.asiaalliedgroup.com/en")
    with pytest.raises(urllib.error.HTTPError, match="cross-origin redirect blocked"):
        handler.redirect_request(
            request,
            None,
            302,
            "Found",
            {},
            "http://169.254.169.254/latest/meta-data",
        )

    with pytest.raises(ValueError, match="out-of-scope URLs"):
        select_representative_pages(
            {
                "en": [
                    "https://www.asiaalliedgroup.com/en",
                    "https://evil.example/injected",
                ]
            }
        )


def test_route_normalization_only_collapses_content_detail_dimensions() -> None:
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/blog/01/tag/infrastructure"
        )
        == "blog/{month}/tag/{slug}"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/blog/2026/example-article"
        )
        == "blog/{year}/{slug}"
    )
    assert (
        normalized_route_signature("https://www.asiaalliedgroup.com/en/blog/2026/01")
        == "blog/{year}/{month}"
    )
    assert (
        normalized_route_signature("https://www.asiaalliedgroup.com/en/blog/csr/12")
        == "blog/csr/{month}"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/blog/csr/tag/csr"
        )
        == "blog/csr/tag/{slug}"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/investor-relations/financial-reports"
        )
        == "investor-relations/financial-reports"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/investor-relations/stock-chart"
        )
        == "investor-relations/stock-chart"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/projects/construction"
        )
        == "projects/construction"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/services/engineering"
        )
        == "services/engineering"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/services/property-management"
        )
        == "services/property-management"
    )
    assert (
        normalized_route_signature(
            "https://www.asiaalliedgroup.com/en/career/project-manager-j2026081901"
        )
        == "career/{slug}"
    )


def test_sitemap_and_template_audit_is_complete_and_error_free() -> None:
    audit = load_json(EVIDENCE / "site-map-and-template-audit.json")
    scope = audit["scope"]

    assert scope["total_sitemap_entries"] == 10_669
    assert scope["total_unique_sitemap_urls"] == 10_666
    assert scope["normalized_route_signature_count"] == 559
    assert scope["representative_page_count"] == 559
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
    assert len(pages) == 559
    assert {
        locale: sum(page["locale"] == locale for page in pages)
        for locale in ("en", "tc", "sc")
    } == {"en": 188, "tc": 175, "sc": 196}
    assert all(page["status"] == 200 for page in pages)
    assert {page["locale"] for page in pages} == {"en", "tc", "sc"}
    expected_signatures = {
        (locale, signature)
        for locale, sitemap in scope["sitemaps"].items()
        for signature in sitemap["normalized_route_signatures"]
    }
    observed_signatures = {(page["locale"], page["route_signature"]) for page in pages}
    assert observed_signatures == expected_signatures
    assert ("en", "blog/{slug}/tag/{slug}") not in observed_signatures
    assert ("en", "blog/csr/tag/{slug}") in observed_signatures
    protected = {
        "investor-relations/corporate-governance",
        "investor-relations/financial-reports",
        "investor-relations/stock-chart",
        "projects/construction",
        "projects/professional-services",
        "the-group/about-the-group",
        "the-group/vision-mission-and-core-values",
    }
    assert protected <= {
        signature for locale, signature in observed_signatures if locale == "en"
    }


def test_source_evidence_index_covers_every_token_and_component() -> None:
    evidence = load_json(EVIDENCE / "source-evidence-index.json")
    assert len(evidence["token_evidence"]) == 62
    assert len(evidence["public_component_evidence"]) == 52
    assert evidence["token_evidence"]["colors.text-on-accent"]["classification"] == (
        "accessibility-correction"
    )
    assert (
        evidence["token_evidence"]["colors.accent-accessible"]["classification"]
        == "accessibility-correction"
    )
    assert not any(
        record["classification"] == "observed-exact"
        for record in evidence["token_evidence"].values()
    )

    for token, record in evidence["token_evidence"].items():
        assert token
        assert record["classification"]
        assert record["source_stylesheets"]
        assert record["live_page_locations"] == []
        assert record["computed_style_evidence_ref"] is None
        assert record["evidence_methods"]
        exact_urls = {
            item["source_url"]
            for item in (
                *record.get("css_declarations", []),
                *record.get("media_queries", []),
            )
        }
        has_css_evidence = bool(exact_urls)
        if has_css_evidence:
            assert record["primary_evidence_url"] in exact_urls
            assert set(record["cross_check_urls"]) <= exact_urls
            if record.get("media_queries"):
                assert record["viewport_scope"] == ["source-css-media-query"]
                assert record["state_scope"] == ["source-css-media-query"]
                assert record["evidence_methods"] == [
                    "public-css-media-query-extraction"
                ]
            else:
                assert record["viewport_scope"] == []
                assert record["state_scope"] == ["source-css-declaration"]
                assert record["evidence_methods"] == [
                    "public-css-declaration-extraction"
                ]
        else:
            assert record["primary_evidence_url"] is None
            assert record["viewport_scope"] == []
            assert record["state_scope"] == ["not-observed"]
            assert "exact source value not observed" in record["evidence_methods"][0]

    for component, record in evidence["public_component_evidence"].items():
        assert component
        assert record["classification"]
        assert record["markers"]
        assert record["viewport_scope"] == []
        assert isinstance(record["state_evidence"], dict)
        assert record["computed_style_evidence_ref"] is None
        assert record["evidence_methods"] or record["classification"] == "not-observed"
        assert (
            record["live_page_locations"]
            or record["css_selector_evidence"]
            or record["classification"] == "not-observed"
        )
        for location in record["live_page_locations"]:
            assert is_allowed_source_url(location["url"])
            assert location["page_location"]
            assert location["page_title"] is not None


def test_human_evidence_register_does_not_overclaim_normalized_live_states() -> None:
    renderer = (ROOT / "scripts" / "render_design_evidence.py").read_text(
        encoding="utf-8"
    )
    assert "strict=False" not in renderer
    assert renderer.count("strict=True") >= 2
    register = (ROOT / "docs" / "design-system" / "source-evidence.md").read_text(
        encoding="utf-8"
    )
    for variant in ("page-canvas", "status-success", "accent-surface-large"):
        line = next(
            line
            for line in register.splitlines()
            if line.startswith(f"| `{variant}` |")
        )
        assert "normalized variant not observed live" in line
        assert "rendered default observed" not in line
    assert "| `button-primary-disabled` |" in register
    assert "`not observed as live state`" in register
    assert "Rendered profile/viewport records: `129`" in register
    assert "Successful visible state samples: `255`" in register
    assert "Rendered responsive states" not in register


def test_computed_style_collector_is_same_origin_and_visible_only() -> None:
    collector = (ROOT / "scripts" / "audit_aai_computed_styles.mjs").read_text(
        encoding="utf-8"
    )
    policy = (ROOT / "scripts" / "aai_browser_network_policy.mjs").read_text(
        encoding="utf-8"
    )
    assert "applyBrowserNetworkPolicy(context" in collector
    assert "browserContextOptions({ viewport, locale })" in collector
    assert "serviceWorkers: 'block'" in policy
    assert "context.routeWebSocket('**/*'" in policy
    assert "webSocketRoute.connectToServer()" in policy
    assert "webSocketRoute.close({ code: 1008" in policy
    assert "route.abort('blockedbyclient')" in policy
    assert "Cross-origin final URL blocked" in collector
    assert "Cross-origin retry URL blocked" in collector
    assert "candidates.evaluateAll" in collector
    assert "Execution context was destroyed" in collector
    assert "const selectedProfiles = profileFilter" in collector
    assert ".first()" not in collector


def test_computed_style_walkthrough_covers_all_profiles_and_viewports() -> None:
    evidence = load_json(EVIDENCE / "computed-style-walkthrough.json")
    assert evidence["schemaVersion"] == 2
    assert "visible elements" in evidence["methodology"]
    assert "exact https://www.asiaalliedgroup.com origin" in evidence["networkScope"]
    required_profiles = {
        "investor-governance",
        "investor-reports",
        "investor-stock-chart",
        "project-construction",
        "project-professional-services",
        "group-about",
        "group-vision",
        "tc-home",
        "tc-group-about",
        "tc-investor-reports",
        "tc-publication-list",
        "tc-projects-list",
        "tc-contact-form",
        "sc-home",
        "sc-group-about",
        "sc-investor-reports",
        "sc-publication-list",
        "sc-projects-list",
        "sc-contact-form",
    }
    assert required_profiles <= {item["name"] for item in evidence["profiles"]}
    assert {item["name"] for item in evidence["viewports"]} == {
        "desktop",
        "tablet",
        "mobile",
    }
    assert evidence["resultCount"] == len(evidence["profiles"]) * 3
    assert evidence["failureCount"] == 0
    assert not evidence["failures"]
    assert all(item["status"] == 200 for item in evidence["results"])
    assert not any(item["horizontalOverflow"] for item in evidence["results"])
    sampled_elements = [
        sample
        for result in evidence["results"]
        for sample in (*result["styles"].values(), *result["states"].values())
        if sample is not None
    ]
    assert sampled_elements
    assert all(sample["visible"] for sample in sampled_elements)
    assert all(not sample["hidden"] for sample in sampled_elements)
    assert all(sample["values"]["display"] != "none" for sample in sampled_elements)
    assert all(
        sample["values"]["visibility"] != "hidden" for sample in sampled_elements
    )
    state_hits = {
        state: sum(state in result["states"] for result in evidence["results"])
        for state in {
            state for result in evidence["results"] for state in result["states"]
        }
    }
    for state in ("buttonHover", "buttonFocus", "buttonActive"):
        assert state_hits.get(state, 0) > 0


def test_stylesheet_evidence_has_expected_hashes_and_brand_values() -> None:
    evidence = load_json(EVIDENCE / "css-token-evidence.json")
    assert "bounded" in evidence["provenance"]["excerpt_policy"]
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
    assert any("338px" in query for query in project["media_queries"])
    assert any("1679px" in query for query in project["media_queries"])
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


def test_component_contract_evidence_resolves_to_direct_source_records() -> None:
    contracts = load_json(ROOT / "design-system" / "components.json")
    source_index = load_json(EVIDENCE / "source-evidence-index.json")
    public_components = source_index["public_component_evidence"]
    failures: list[str] = []

    evidence_blocks: list[tuple[str, dict[str, Any]]] = []
    for name, contract in contracts["behavior_contracts"].items():
        evidence_blocks.append((f"behavior_contracts.{name}", contract["evidence"]))
    for name, evidence in contracts["visual_component_evidence"].items():
        evidence_blocks.append((f"visual_component_evidence.{name}", evidence))

    for path, evidence in evidence_blocks:
        refs = evidence["sourceComponents"]
        urls = evidence["sourceUrls"]
        locations = evidence["pageLocations"]
        missing_refs = sorted(set(refs) - set(public_components))
        if missing_refs:
            failures.append(f"{path}: unknown sourceComponents {missing_refs}")
            continue
        allowed_urls: set[str] = set()
        for ref in refs:
            record = public_components[ref]
            allowed_urls.update(
                location["url"] for location in record["live_page_locations"]
            )
            allowed_urls.update(
                item["source_url"] for item in record["css_selector_evidence"]
            )
        invalid_urls = sorted(set(urls) - allowed_urls)
        if invalid_urls:
            failures.append(
                f"{path}: URLs without direct referenced evidence {invalid_urls}"
            )
        if len(urls) != len(locations):
            failures.append(
                f"{path}: sourceUrls/pageLocations length mismatch "
                f"{len(urls)} != {len(locations)}"
            )
            continue
        direct_pairs: set[tuple[str, str]] = set()
        css_urls: set[str] = set()
        for ref in refs:
            record = public_components[ref]
            direct_pairs.update(
                (location["url"], location["page_location"])
                for location in record["live_page_locations"]
            )
            css_urls.update(
                item["source_url"] for item in record["css_selector_evidence"]
            )
        for url, location in zip(urls, locations, strict=True):
            if (url, location) in direct_pairs:
                continue
            if location == "not observed" and url in css_urls:
                continue
            failures.append(
                f"{path}: URL/location pair is not a direct record "
                f"({url!r}, {location!r})"
            )

    assert failures == []


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
    assert len(extension_components) == 31
    assert components["components"] == extension_components
    assert len(components["behavior_contracts"]) >= 28
    assert (
        components["behavior_contracts"]
        == dtcg["$extensions"][EXTENSION_KEY]["componentBehavior"]
    )
    assert (
        components["implementation_coverage"]
        == dtcg["$extensions"][EXTENSION_KEY]["componentImplementation"]
    )
    assert set(components["implementation_coverage"]) == set(
        components["behavior_contracts"]
    )
    for family, contract in components["behavior_contracts"].items():
        mappings = components["implementation_coverage"][family]["stateMappings"]
        assert len(mappings) == len(contract["variants"]) * len(contract["states"])
        for mapping in mappings.values():
            assert mapping["status"] in {"mapped", "behavior-only"}
            if mapping["status"] == "mapped":
                assert mapping["styleRef"] in components["components"]
            else:
                assert mapping["note"]
    assert set(components["visual_component_evidence"]) == set(components["components"])
    for evidence in components["visual_component_evidence"].values():
        assert evidence["classification"]
        assert evidence["sourceComponents"]
        assert evidence["sourceUrls"]
        assert evidence["pageLocations"]
    for contract in components["behavior_contracts"].values():
        evidence = contract["evidence"]
        assert evidence["classification"]
        assert evidence["sourceComponents"]
        assert evidence["sourceUrls"]
        assert evidence["pageLocations"]

    assert tailwind["theme"]["extend"]["screens"] == {
        "compact": "370px",
        "sm": "576px",
        "md": "768px",
        "lg": "992px",
        "xl": "1200px",
        "2xl": "1600px",
    }
    assert tailwind["theme"]["extend"]["maxWidth"]["container-2xl"] == "1570px"
    assert tailwind["theme"]["extend"]["boxShadow"]["low"] == (
        "0 4px 12px rgba(0, 0, 0, 0.10)"
    )

    theme_css = (ROOT / "design-system" / "theme.css").read_text(encoding="utf-8")
    css_colors = dict(re.findall(r"--color-([a-z0-9-]+):\s*(#[0-9a-f]{6});", theme_css))
    assert css_colors == EXPECTED_COLORS
    assert '--font-display-lg: "Pragati Narrow", "Noto Sans TC"' in theme_css
    assert '--font-body-md: "Roboto", "Noto Sans TC"' in theme_css
    assert '"Pragati Narrow, Roboto' not in theme_css
    for name, line_height in EXPECTED_LINE_HEIGHTS.items():
        assert f"--leading-{name}: {line_height};" in theme_css

    foundation = (ROOT / "design-system" / "foundation.css").read_text(encoding="utf-8")
    assert foundation.startswith(":root {")
    assert "--color-primary: #006a63;" in foundation
    assert (
        '--font-body: "Roboto", "Noto Sans TC", "Microsoft JhengHei", Arial, sans-serif;'
        in foundation
    )
    assert "--breakpoint-2xl: 1600px;" in foundation
    assert ".type-body-md {" in foundation
    assert "font-weight: var(--weight-body-md);" in foundation
    assert tailwind["theme"]["extend"]["fontFamily"]["body-md"][:2] == [
        "Roboto",
        "Noto Sans TC",
    ]

    preset = (ROOT / "design-system" / "tailwind.preset.cjs").read_text(
        encoding="utf-8"
    )
    assert preset.startswith(
        "// Generated from DESIGN.md. Do not edit.\nmodule.exports = "
    )


def test_pen_visual_board_is_derived_from_normative_artifacts() -> None:
    import hashlib

    pen = load_json(ROOT / "design-system" / "asia-allied-design-system.pen")
    tokens = load_json(ROOT / "design-system" / "tokens.json")
    contracts = load_json(ROOT / "design-system" / "components.json")

    def walk(node: dict[str, Any]) -> list[dict[str, Any]]:
        descendants = [node]
        for child in node.get("children", []):
            descendants.extend(walk(child))
        return descendants

    nodes = [node for board in pen["children"] for node in walk(board)]
    nodes_by_id = {node["id"]: node for node in nodes}

    assert len(nodes_by_id) == len(nodes)
    assert pen["version"] == "2.17"
    assert pen["children"][0]["metadata"] == {
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
        "inputSha256": {
            "DESIGN.md": hashlib.sha256((ROOT / "DESIGN.md").read_bytes()).hexdigest(),
            "design-system/tokens.json": hashlib.sha256(
                (ROOT / "design-system" / "tokens.json").read_bytes()
            ).hexdigest(),
            "design-system/components.json": hashlib.sha256(
                (ROOT / "design-system" / "components.json").read_bytes()
            ).hexdigest(),
        },
    }
    assert pen["variables"]["color-primary"]["value"] == "#006a63"
    assert pen["variables"]["color-accent"]["value"] == "#e6762d"
    assert {child["name"] for child in pen["children"]} == {
        "Cover",
        "Color tokens",
        "Contrast and color accessibility",
        "Typography roles",
        "Localization and type rules",
        "Layout and spacing",
        "Elevation, motion and shapes",
        "Visual contracts · actions and forms",
        "Visual contracts · surfaces and status",
        "Behavior · actions and navigation",
        "Behavior · forms and selection",
        "Behavior · content and data",
        "Behavior · feedback and system",
        "Variant and state implementation",
        "Accessibility, icons and assets",
        "Responsive compositions",
        "Page patterns and adaptation",
        "Evidence and provenance",
        "Coverage and limitations",
        "Do and don't",
    }

    for name in (name for name in tokens["color"] if not name.startswith("$")):
        node = nodes_by_id[f"color-card-{name}"]
        child_ids = {child["id"] for child in node["children"]}
        assert {
            f"color-card-{name}-role",
            f"color-card-{name}-classification",
            f"color-card-{name}-usage",
        } <= child_ids
    for name in (name for name in tokens["typography"] if not name.startswith("$")):
        assert f"type-row-{name}" in nodes_by_id
        assert f"type-row-{name}-metrics" in nodes_by_id
    for name in (name for name in tokens["spacing"] if not name.startswith("$")):
        assert f"space-row-{name}" in nodes_by_id
    for name in (name for name in tokens["rounded"] if not name.startswith("$")):
        assert f"radius-{name}" in nodes_by_id
    assert {
        f"breakpoint-{name}" for name in ("compact", "sm", "md", "lg", "xl", "2xl")
    } <= set(nodes_by_id)
    assert {f"container-{name}" for name in ("sm", "md", "lg", "xl", "2xl")} <= set(
        nodes_by_id
    )
    assert {"elevation-none", "elevation-low"} <= set(nodes_by_id)
    assert {
        "motion-duration-fast",
        "motion-duration-standard",
        "motion-duration-brand",
        "motion-easing-standard",
        "motion-easing-brand",
    } <= set(nodes_by_id)

    for name in contracts["components"]:
        node = nodes_by_id[f"visual-{name}"]
        assert node["metadata"]["contractName"] == name
        assert node["metadata"]["contractType"] == "visual"
        assert node["metadata"]["component"] == contracts["components"][name]
        assert (
            node["metadata"]["evidence"] == contracts["visual_component_evidence"][name]
        )
        assert f"visual-{name}-values" in {child["id"] for child in node["children"]}

    for name in contracts["behavior_contracts"]:
        node = nodes_by_id[f"behavior-{name}"]
        assert node["metadata"]["contractName"] == name
        assert node["metadata"]["contractType"] == "behavior"
        assert (
            node["metadata"]["variants"]
            == contracts["behavior_contracts"][name]["variants"]
        )
        assert (
            node["metadata"]["states"]
            == contracts["behavior_contracts"][name]["states"]
        )
        assert (
            node["metadata"]["requirements"]
            == contracts["behavior_contracts"][name]["requirements"]
        )
        assert (
            node["metadata"]["implementationCoverage"]
            == contracts["implementation_coverage"][name]
        )
        child_ids = {child["id"] for child in node["children"]}
        assert {
            f"behavior-{name}-preview",
            f"behavior-{name}-variants",
            f"behavior-{name}-states",
            f"behavior-{name}-requirements",
            f"behavior-{name}-evidence",
            f"behavior-{name}-coverage",
        } <= child_ids

        for requirement in contracts["behavior_contracts"][name]["requirements"]:
            assert f"requirement-{name}-{requirement}" in nodes_by_id

        for pair, mapping in contracts["implementation_coverage"][name][
            "stateMappings"
        ].items():
            variant, state = pair.split(".", 1)
            cell = nodes_by_id[f"coverage-cell-{name}-{variant}-{state}"]
            assert cell["metadata"] == mapping

    assert {"responsive-desktop", "responsive-tablet", "responsive-mobile"} <= set(
        nodes_by_id
    )
    assert {
        "contrast-white-primary",
        "contrast-white-primary-dark",
        "contrast-white-accent",
        "contrast-white-accent-accessible",
        "contrast-white-accent-selected",
        "contrast-text-white",
        "contrast-text-muted-white",
        "contrast-danger-white",
        "type-sample-en",
        "type-sample-tc",
        "type-sample-long",
        "assets-svg-icons",
        "assets-icon-font",
        "assets-licensing",
        "assets-imagery",
        "evidence-observed",
        "evidence-cross-page",
        "evidence-normalized",
        "evidence-accessibility",
        "evidence-not-observed",
        "coverage-sitemap",
        "coverage-http",
        "coverage-browser",
        "guidance-do",
        "guidance-dont",
    } <= set(nodes_by_id)
    assert {f"guidance-do-{index}" for index in range(8)} <= set(nodes_by_id)
    assert {f"guidance-dont-{index}" for index in range(8)} <= set(nodes_by_id)
    assert {
        f"page-pattern-{name}"
        for name in (
            "home",
            "group",
            "investor-static",
            "publication-list",
            "publication-detail",
            "project-sector",
            "project-list",
            "project-detail",
            "job",
            "form",
            "legal",
        )
    } <= set(nodes_by_id)

    coverage = contracts["implementation_coverage"]
    state_statuses = [
        mapping["status"]
        for component in coverage.values()
        for mapping in component["stateMappings"].values()
    ]
    assert nodes_by_id["coverage"]["metadata"] == {
        "behaviorContracts": 31,
        "visualContracts": 31,
        "variantStateMappings": len(state_statuses),
        "mapped": state_statuses.count("mapped"),
        "behaviorOnly": state_statuses.count("behavior-only"),
    }

    readme = (ROOT / "design-system" / "README.md").read_text(encoding="utf-8")
    assert "Complete 20-board visual derivative" in readme
    assert "20 separated boards" in readme


def test_runtime_frontend_consumes_the_normative_foundation() -> None:
    styles = (ROOT / "frontend" / "src" / "styles.css").read_text(encoding="utf-8")
    compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
    dockerfile = (ROOT / "frontend" / "Dockerfile").read_text(encoding="utf-8")
    assert '@import "../../design-system/foundation.css";' in styles
    assert "context: ." in compose
    assert "dockerfile: frontend/Dockerfile" in compose
    assert (
        "COPY design-system/foundation.css ../design-system/foundation.css"
        in dockerfile
    )
    assert "COPY --from=builder /workspace/frontend/dist" in dockerfile
    assert "Inter" not in styles
    assert "#174ea6" not in styles.lower()
    assert "border-radius:14px" not in styles.replace(" ", "")
    assert "var(--color-primary)" in styles


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
