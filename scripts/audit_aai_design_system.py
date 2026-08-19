"""Audit the public Asia Allied website's design-system evidence.

This script exhaustively parses the three published sitemaps, then fetches a
bounded, deterministic set of representative page templates. It records facts
and selector evidence; it does not copy the source website's CSS or assets into
the repository.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml

BASE_URL = "https://www.asiaalliedgroup.com"
SITEMAPS = {
    "en": f"{BASE_URL}/sitemap.xml",
    "tc": f"{BASE_URL}/sitemap-tc.xml",
    "sc": f"{BASE_URL}/sitemap-sc.xml",
}
ROBOTS_URL = f"{BASE_URL}/robots.txt"
USER_AGENT = (
    "CompanyScaffold-DesignAudit/1.0 "
    "(+https://github.com/corgimomo2023/company-fullstack-scaffold)"
)
EXPECTED_STYLESHEETS = {
    f"{BASE_URL}/assets/css/projectbase.css",
    f"{BASE_URL}/assets/css/print.css",
}
CONTENT_DETAIL_ROOTS = {
    "blog",
    "board-of-director",
    "career",
    "directors",
    "enews",
    "media-coverage",
    "press-release",
}
COMPONENT_MARKERS = {
    "site-header": ("header", "page-head", "header__"),
    "utility-navigation": ("header-top", "utility", "lang"),
    "site-search": ("sitesearch", "site-search"),
    "desktop-navigation": ("mn__nav", "mn__list", "mn__link"),
    "mobile-navigation": ("mb-mn__wrap", "mTrigger__open"),
    "breadcrumbs": ("breadcrumb",),
    "page-title": ("page-title-wrap", "page-title"),
    "page-menu": ("page-menu__link", "page-menu"),
    "page-tabs": ("blk-tab__list", "blk-tab__btn", "tab__select"),
    "filter-bar": ("filter", "filter__row", "filter__blk--year"),
    "hero-carousel": ("key-visual", "slick-slider"),
    "image-title-card": ("img-title-blk",),
    "image-card": ("img-card-blk",),
    "image-overlay-card": ("img-overlay-blk",),
    "overlay-cover-card": ("overlay-cover-blk",),
    "image-plate": ("img-plate-blk",),
    "spaced-image-plate": ("img-space-plate-blk",),
    "left-image-card": ("left-img-blk",),
    "top-image-card": ("top-img-blk",),
    "blog-card-list": ("img-blog-blk", "img-blog-list"),
    "thumbnail-list": ("thumb-blk", "thumb-blk-list"),
    "information-tile-card": ("it-blk",),
    "image-slider": ("image-slider", "image-slider__item"),
    "milestone-card": ("milestone-blk",),
    "share-dropdown": ("link-copy-dropdown", "link-copy-dropdown__item"),
    "feature-slider": ("feature-slider",),
    "video-link": ("video-link",),
    "rich-text": ("ckec", "cke_editable", "rte"),
    "tag-filter": ("tag-list", "tag selected", "tag.selected"),
    "custom-select": ("js-selectBox", "multiselect-container"),
    "listing-table": ("listing-table",),
    "pagination": ("pagination", "pager"),
    "load-more": ("js-loadmore",),
    "button": ("btn",),
    "text-input": ("form-control", "fe-form-control"),
    "checkbox-radio": ("checkbox-input", "radio-input", "rc--"),
    "validation": ("is-valid", "is-invalid", "valid-feedback", "invalid-feedback"),
    "form-group": ("fe-form-group", "field__"),
    "subscription-form": ("subscribe-area", "btn-gp__input"),
    "contact-form": ("recaptcha", "contact-form"),
    "year-accordion": ("rte-year-collapse",),
    "development-timeline": ("history-year-blk",),
    "corporate-structure": ("tree-structure", "node-name"),
    "global-footprint-map": ("f-map", "f-map__dot"),
    "document-download": ("download", "report"),
    "director-person": ("director", "people"),
    "job-listing": ("job-d__apply", "career"),
    "publication": ("press-release", "enews", "media-coverage"),
    "project-list-detail": ("project-d", "projects"),
    "social-links": ("soc-sq", "social"),
    "back-to-top": ("bk2Top",),
    "footer": ("footer", "contact-bottom"),
}

HEX_RE = re.compile(
    r"(?<![\w-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])"
)
RGB_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
MEDIA_RE = re.compile(r"@media(?:\s+[^{(]+)?\s*\(([^)]*)\)", re.IGNORECASE)
FONT_FACE_RE = re.compile(r"@font-face\s*\{([^{}]*)\}", re.IGNORECASE | re.DOTALL)


@dataclass
class PageFacts:
    title: str = ""
    html_lang: str = ""
    stylesheets: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    classes: collections.Counter[str] = field(default_factory=collections.Counter)
    ids: collections.Counter[str] = field(default_factory=collections.Counter)
    tags: collections.Counter[str] = field(default_factory=collections.Counter)
    semantic_counts: collections.Counter[str] = field(
        default_factory=collections.Counter
    )


class FactsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.facts = PageFacts()
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        self.facts.tags[tag] += 1
        if tag in {"header", "nav", "main", "footer", "form", "table", "dialog"}:
            self.facts.semantic_counts[tag] += 1
        if tag == "html":
            self.facts.html_lang = attrs_d.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "link" and "stylesheet" in attrs_d.get("rel", "").lower():
            href = attrs_d.get("href")
            if href:
                self.facts.stylesheets.append(href)
        if tag == "script" and attrs_d.get("src"):
            self.facts.scripts.append(attrs_d["src"])
        for name in attrs_d.get("class", "").split():
            self.facts.classes[name] += 1
        if attrs_d.get("id"):
            self.facts.ids[attrs_d["id"]] += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False
            self.facts.title = " ".join("".join(self._title_parts).split())

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)


class SameOriginRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects that leave the exact audited HTTPS origin."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> urllib.request.Request | None:
        target = urllib.parse.urljoin(req.full_url, newurl)
        if not is_allowed_source_url(target):
            raise urllib.error.HTTPError(
                target,
                code,
                "cross-origin redirect blocked",
                headers,
                fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, target)


SAFE_OPENER = urllib.request.build_opener(SameOriginRedirectHandler())


def fetch(url: str, *, retries: int = 3) -> tuple[bytes, dict[str, str], int, str]:
    if not is_allowed_source_url(url):
        raise ValueError(f"URL is outside the audited HTTPS origin: {url}")
    safe_url = urllib.parse.quote(url, safe=":/?&=%#[]!$'()*+,;@~")
    request = urllib.request.Request(
        safe_url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,text/css;q=0.8,*/*;q=0.5",
            "Accept-Language": "en,zh-HK;q=0.8,zh-CN;q=0.6",
        },
    )
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with SAFE_OPENER.open(request, timeout=30) as response:
                final_url = response.geturl()
                if not is_allowed_source_url(final_url):
                    raise ValueError(
                        f"Final URL is outside the audited HTTPS origin: {final_url}"
                    )
                return (
                    response.read(),
                    {k.lower(): v for k, v in response.headers.items()},
                    response.status,
                    final_url,
                )
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt + 1 < retries:
                time.sleep(0.5 * (2**attempt))
    assert last_error is not None
    raise last_error


def normalize_url(url: str, base: str = BASE_URL) -> str:
    absolute = urllib.parse.urljoin(base, url)
    parts = urllib.parse.urlsplit(absolute)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def is_allowed_source_url(url: str) -> bool:
    """Return whether a normalized URL belongs to the audited HTTPS origin."""
    parts = urllib.parse.urlsplit(url)
    source = urllib.parse.urlsplit(BASE_URL)
    return parts.scheme == source.scheme and parts.netloc == source.netloc


def normalize_hex(value: str) -> str:
    value = value.upper()
    if len(value) in {4, 5}:
        value = "#" + "".join(char * 2 for char in value[1:])
    return value


def parse_sitemap(data: bytes) -> list[str]:
    root = ET.fromstring(data)
    return [
        node.text.strip()
        for node in root.iter()
        if node.tag.endswith("loc") and node.text and node.text.strip()
    ]


def locale_neutral_parts(url: str) -> list[str]:
    path = urllib.parse.unquote(urllib.parse.urlsplit(url).path).strip("/")
    parts = [part for part in path.split("/") if part]
    if parts and parts[0] in {"en", "tc", "sc"}:
        parts = parts[1:]
    return parts


def normalized_route_signature(url: str) -> str:
    """Normalize only explicitly classified content-detail/archive routes."""
    parts = locale_neutral_parts(url)
    content_route = bool(parts and parts[0] in CONTENT_DETAIL_ROOTS)
    signature_parts: list[str] = []
    for index, part in enumerate(parts):
        is_last_part = index == len(parts) - 1
        if content_route and re.fullmatch(r"(?:19|20)\d{2}", part):
            signature_parts.append("{year}")
        elif parts and parts[0] == "blog" and re.fullmatch(r"(?:0[1-9]|1[0-2])", part):
            signature_parts.append("{month}")
        elif content_route and re.fullmatch(r"page\d+", part):
            signature_parts.append("{page}")
        elif content_route and is_last_part and part.isdigit() and len(parts) >= 2:
            signature_parts.append("{id}")
        elif content_route and is_last_part and len(parts) >= 2:
            signature_parts.append("{slug}")
        else:
            signature_parts.append(part)
    return "/".join(signature_parts) or "home"


def sitemap_inventory(urls: list[str]) -> dict[str, Any]:
    categories: collections.Counter[str] = collections.Counter()
    depths: collections.Counter[int] = collections.Counter()
    signatures: collections.Counter[str] = collections.Counter()
    invalid: list[str] = []
    for url in urls:
        parts = locale_neutral_parts(url)
        category = parts[0] if parts else "home"
        categories[category] += 1
        depths[len(parts)] += 1
        signatures[normalized_route_signature(url)] += 1
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "www.asiaalliedgroup.com":
            invalid.append(url)
    url_counts = collections.Counter(urls)
    duplicate_urls = {
        url: count for url, count in sorted(url_counts.items()) if count > 1
    }
    duplicates = len(urls) - len(set(urls))
    return {
        "url_count": len(urls),
        "unique_url_count": len(set(urls)),
        "duplicate_count": duplicates,
        "duplicate_urls": duplicate_urls,
        "invalid_scope_urls": sorted(set(invalid)),
        "categories": dict(sorted(categories.items())),
        "depths": {str(k): v for k, v in sorted(depths.items())},
        "normalized_route_signatures": dict(sorted(signatures.items())),
    }


def select_representative_pages(
    sitemaps: dict[str, list[str]],
) -> list[tuple[str, str, str]]:
    selected: list[tuple[str, str, str]] = []
    seen_signatures: set[tuple[str, str]] = set()
    for locale, urls in sitemaps.items():
        invalid = [url for url in urls if not is_allowed_source_url(url)]
        if invalid:
            raise ValueError(
                f"Sitemap {locale} contains out-of-scope URLs: {invalid[:3]}"
            )
        for url in sorted(set(urls)):
            route_signature = normalized_route_signature(url)
            locale_signature = (locale, route_signature)
            if locale_signature in seen_signatures:
                continue
            seen_signatures.add(locale_signature)
            selected.append((locale, route_signature, url))
    return selected


def parse_css(css: str, source_url: str) -> dict[str, Any]:
    color_evidence: dict[str, dict[str, Any]] = collections.defaultdict(
        lambda: {"count": 0, "properties": collections.Counter(), "evidence": []}
    )
    property_values: dict[str, collections.Counter[str]] = {
        name: collections.Counter()
        for name in (
            "font-family",
            "font-size",
            "font-weight",
            "line-height",
            "letter-spacing",
            "border-radius",
            "box-shadow",
            "transition-duration",
            "transition-timing-function",
            "z-index",
            "max-width",
            "min-width",
            "width",
            "height",
            "margin",
            "margin-top",
            "margin-right",
            "margin-bottom",
            "margin-left",
            "padding",
            "padding-top",
            "padding-right",
            "padding-bottom",
            "padding-left",
            "gap",
        )
    }
    property_evidence: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    component_selector_evidence: dict[str, list[str]] = collections.defaultdict(list)
    component_state_evidence: dict[str, dict[str, list[str]]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    clean = COMMENT_RE.sub("", css)
    rules = 0
    for match in RULE_RE.finditer(clean):
        selector = " ".join(match.group(1).split())
        if selector.startswith("@"):
            continue
        rules += 1
        for component, markers in COMPONENT_MARKERS.items():
            if any(marker in selector for marker in markers):
                evidence = component_selector_evidence[component]
                if selector not in evidence and len(evidence) < 5:
                    evidence.append(selector[:180])
                state_patterns = {
                    "hover": (":hover",),
                    "focus": (":focus", ":focus-visible"),
                    "active": (":active", ".active"),
                    "selected": (".selected", "[aria-selected", "[aria-current"),
                    "disabled": (
                        ":disabled",
                        ".disabled",
                        "[disabled",
                        "[aria-disabled",
                    ),
                    "checked": (":checked", ".checked"),
                    "open-expanded": (".open", ".show", "[aria-expanded"),
                }
                matched_state = False
                for state, patterns in state_patterns.items():
                    if any(pattern in selector for pattern in patterns):
                        matched_state = True
                        state_selectors = component_state_evidence[component][state]
                        if selector not in state_selectors and len(state_selectors) < 5:
                            state_selectors.append(selector[:180])
                if not matched_state:
                    state_selectors = component_state_evidence[component]["default"]
                    if selector not in state_selectors and len(state_selectors) < 5:
                        state_selectors.append(selector[:180])
        for raw_decl in match.group(2).split(";"):
            if ":" not in raw_decl:
                continue
            prop, value = raw_decl.split(":", 1)
            prop = prop.strip().lower()
            value = value.strip()
            if prop in property_values:
                property_values[prop][value] += 1
                evidence = property_evidence[prop][value]
                if selector not in evidence and len(evidence) < 3:
                    evidence.append(selector[:180])
            colors = [normalize_hex(item) for item in HEX_RE.findall(value)]
            colors.extend(
                item.lower().replace(" ", "") for item in RGB_RE.findall(value)
            )
            for color in colors:
                item = color_evidence[color]
                item["count"] += 1
                item["properties"][prop] += 1
                evidence = {
                    "selector": selector[:180],
                    "property": prop,
                    "value": value[:120],
                }
                if evidence not in item["evidence"] and len(item["evidence"]) < 3:
                    item["evidence"].append(evidence)
    font_faces: list[dict[str, str]] = []
    for match in FONT_FACE_RE.finditer(css):
        declarations: dict[str, str] = {}
        for raw_decl in match.group(1).split(";"):
            if ":" in raw_decl:
                prop, value = raw_decl.split(":", 1)
                declarations[prop.strip().lower()] = value.strip()
        font_faces.append(
            {
                key: declarations[key]
                for key in ("font-family", "font-weight", "font-style", "font-display")
                if key in declarations
            }
        )
    return {
        "source_url": source_url,
        "sha256": hashlib.sha256(css.encode("utf-8")).hexdigest(),
        "bytes": len(css.encode("utf-8")),
        "parsed_rule_count": rules,
        "font_faces": font_faces,
        "colors": {
            color: {
                "count": item["count"],
                "properties": dict(item["properties"].most_common()),
                "evidence": item["evidence"],
            }
            for color, item in sorted(
                color_evidence.items(), key=lambda pair: (-pair[1]["count"], pair[0])
            )
        },
        "property_values": {
            prop: {
                "unique_value_count": len(counter),
                "top_values": dict(counter.most_common(25)),
                "evidence": {
                    value: property_evidence[prop][value]
                    for value, _count in counter.most_common(25)
                },
            }
            for prop, counter in property_values.items()
        },
        "media_queries": dict(collections.Counter(MEDIA_RE.findall(css)).most_common()),
        "component_selector_hits": {
            component: sum(css.count(marker) for marker in markers)
            for component, markers in COMPONENT_MARKERS.items()
        },
        "component_selector_evidence": dict(component_selector_evidence),
        "component_state_evidence": {
            component: dict(states)
            for component, states in component_state_evidence.items()
        },
    }


def page_component_hits(facts: PageFacts) -> dict[str, int]:
    def marker_count(marker: str) -> int:
        tokens = [
            token for token in marker.lstrip(".#").replace(".", " ").split() if token
        ]
        if len(tokens) > 1:
            counts = [facts.classes.get(token, 0) for token in tokens]
            return min(counts) if all(counts) else 0
        token = tokens[0]
        exact = facts.classes.get(token, 0) + facts.ids.get(token, 0)
        prefixed = sum(
            count
            for name, count in (*facts.classes.items(), *facts.ids.items())
            if name.startswith((f"{token}__", f"{token}--"))
        )
        return exact + prefixed + facts.tags.get(token, 0)

    return {
        component: sum(marker_count(marker) for marker in markers)
        for component, markers in COMPONENT_MARKERS.items()
        if any(marker_count(marker) for marker in markers)
    }


def load_normative_design() -> dict[str, Any]:
    design_path = Path(__file__).resolve().parents[1] / "DESIGN.md"
    text = design_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError("DESIGN.md has no YAML front matter")
    design = yaml.safe_load(match.group(1))
    if not isinstance(design, dict):
        raise TypeError("DESIGN.md front matter must be a mapping")
    return design


def css_property_evidence(
    css_results: list[dict[str, Any]],
    properties: tuple[str, ...],
    target: Any,
    *,
    contains: bool = False,
) -> list[dict[str, Any]]:
    target_text = str(target).strip().lower()
    evidence: list[dict[str, Any]] = []
    for stylesheet in css_results:
        for prop in properties:
            values = stylesheet.get("property_values", {}).get(prop, {})
            for value, selectors in values.get("evidence", {}).items():
                value_text = value.strip().lower()
                matched = (
                    target_text in value_text if contains else target_text == value_text
                )
                if not matched:
                    continue
                evidence.append(
                    {
                        "source_url": stylesheet["source_url"],
                        "property": prop,
                        "value": value,
                        "selectors": selectors,
                    }
                )
    return evidence


def build_source_evidence_index(
    audit_date: str,
    page_results: list[dict[str, Any]],
    css_results: list[dict[str, Any]],
) -> dict[str, Any]:
    design = load_normative_design()
    stylesheet_urls = [
        item["source_url"] for item in css_results if item.get("status") != "error"
    ]
    token_index: dict[str, dict[str, Any]] = {}

    for name, value in design["colors"].items():
        normalized = normalize_hex(str(value))
        declarations: list[dict[str, Any]] = []
        for stylesheet in css_results:
            color = stylesheet.get("colors", {}).get(normalized)
            if color:
                declarations.append(
                    {
                        "source_url": stylesheet["source_url"],
                        "count": color["count"],
                        "properties": color["properties"],
                        "selectors": color["evidence"],
                    }
                )
        token_index[f"colors.{name}"] = {
            "value": value,
            "classification": (
                "accessibility-correction"
                if name in {"accent-accessible", "text-on-accent"}
                else "normalized-semantic-from-observed-value"
                if declarations
                else "normalized-scaffold-token"
            ),
            "source_stylesheets": stylesheet_urls,
            "css_declarations": declarations,
            "live_page_locations": [],
        }

    typography_props = {
        "fontFamily": ("font-family",),
        "fontSize": ("font-size",),
        "fontWeight": ("font-weight",),
        "lineHeight": ("line-height",),
        "letterSpacing": ("letter-spacing",),
    }
    for name, spec in design["typography"].items():
        declarations: list[dict[str, Any]] = []
        for typography_field, properties in typography_props.items():
            declarations.extend(
                css_property_evidence(
                    css_results,
                    properties,
                    spec[typography_field],
                    contains=typography_field == "fontFamily",
                )
            )
        token_index[f"typography.{name}"] = {
            "value": spec,
            "classification": "normalized-composite-from-observed-css",
            "source_stylesheets": stylesheet_urls,
            "css_declarations": declarations,
            "live_page_locations": [],
        }

    company = {
        item["name"]: item["values"] for item in design["x-exporter-config"]["groups"]
    }
    property_groups = {
        "rounded": (design["rounded"], ("border-radius",)),
        "spacing": (
            design["spacing"],
            (
                "margin",
                "margin-top",
                "margin-right",
                "margin-bottom",
                "margin-left",
                "padding",
                "padding-top",
                "padding-right",
                "padding-bottom",
                "padding-left",
                "gap",
            ),
        ),
        "containers": (company["containers"], ("max-width", "width")),
        "elevation": (company["elevation"], ("box-shadow",)),
        "motion": (
            company["motion"],
            ("transition-duration", "transition-timing-function"),
        ),
    }
    for group, (tokens, properties) in property_groups.items():
        for name, value in tokens.items():
            declarations = css_property_evidence(css_results, properties, value)
            token_index[f"{group}.{name}"] = {
                "value": value,
                "classification": (
                    "normalized-semantic-from-observed-value"
                    if declarations
                    else "normalized-scaffold-token"
                ),
                "source_stylesheets": stylesheet_urls,
                "css_declarations": declarations,
                "live_page_locations": [],
            }

    for name, value in company["breakpoints"].items():
        media_evidence: list[dict[str, Any]] = []
        numeric = re.sub(r"[^0-9.]", "", str(value))
        for stylesheet in css_results:
            for query, count in stylesheet.get("media_queries", {}).items():
                if numeric and numeric in query:
                    media_evidence.append(
                        {
                            "source_url": stylesheet["source_url"],
                            "media_query": query,
                            "count": count,
                        }
                    )
        token_index[f"breakpoints.{name}"] = {
            "value": value,
            "classification": (
                "normalized-semantic-from-observed-media-query"
                if media_evidence
                else "normalized-scaffold-token"
            ),
            "source_stylesheets": stylesheet_urls,
            "media_queries": media_evidence,
            "live_page_locations": [],
        }

    for record in token_index.values():
        exact_evidence = [
            *record.get("css_declarations", []),
            *record.get("media_queries", []),
        ]
        exact_urls = list(dict.fromkeys(item["source_url"] for item in exact_evidence))
        has_css_evidence = bool(exact_urls)
        record["primary_evidence_url"] = exact_urls[0] if exact_urls else None
        record["cross_check_urls"] = exact_urls[1:4]
        record["viewport_scope"] = (
            ["source-css-media-query"] if record.get("media_queries") else []
        )
        record["state_scope"] = (
            ["source-css-media-query"]
            if record.get("media_queries")
            else ["source-css-declaration"]
            if has_css_evidence
            else ["not-observed"]
        )
        record["evidence_methods"] = (
            ["public-css-media-query-extraction"]
            if record.get("media_queries")
            else ["public-css-declaration-extraction"]
            if has_css_evidence
            else ["scaffold-normalization; exact source value not observed"]
        )
        record["computed_style_evidence_ref"] = None
        record["observation_note"] = (
            "Exact raw value/declaration or media query observed; the semantic token name and role are scaffold normalization."
            if has_css_evidence
            else "Normalized scaffold token; exact source/live/computed observation not found."
        )

    component_index: dict[str, dict[str, Any]] = {}
    for component, markers in COMPONENT_MARKERS.items():
        pages = [
            {
                "url": page["url"],
                "final_url": page.get("final_url", page["url"]),
                "page_title": page.get("title"),
                "page_location": f"{page['route_signature']} :: {component}",
                "locale": page["locale"],
                "dom_hit_count": page.get("component_hits", {}).get(component, 0),
            }
            for page in page_results
            if page.get("component_hits", {}).get(component, 0) > 0
        ]
        pages.sort(key=lambda item: (item["locale"] != "en", item["url"]))
        css_evidence = [
            {
                "source_url": stylesheet["source_url"],
                "selector_hit_count": stylesheet.get("component_selector_hits", {}).get(
                    component, 0
                ),
                "selectors": stylesheet.get("component_selector_evidence", {}).get(
                    component, []
                ),
            }
            for stylesheet in css_results
            if stylesheet.get("component_selector_hits", {}).get(component, 0) > 0
        ]
        state_names = {
            state
            for stylesheet in css_results
            for state in stylesheet.get("component_state_evidence", {}).get(
                component, {}
            )
        }
        state_evidence = {
            state: [
                {
                    "source_url": stylesheet["source_url"],
                    "selectors": selectors,
                }
                for stylesheet in css_results
                if (
                    selectors := stylesheet.get("component_state_evidence", {})
                    .get(component, {})
                    .get(state, [])
                )
            ]
            for state in sorted(state_names)
        }
        component_index[component] = {
            "markers": list(markers),
            "classification": (
                "observed-dom-and-css"
                if pages and css_evidence
                else "observed-dom"
                if pages
                else "observed-css-only"
                if css_evidence
                else "not-observed"
            ),
            "live_page_locations": pages[:8],
            "additional_page_location_count": max(0, len(pages) - 8),
            "css_selector_evidence": css_evidence,
            "state_evidence": state_evidence,
            "primary_evidence_url": (
                pages[0]["url"]
                if pages
                else css_evidence[0]["source_url"]
                if css_evidence
                else None
            ),
            "cross_check_urls": [page["url"] for page in pages[1:4]],
            "viewport_scope": [],
            "evidence_methods": [
                method
                for method, available in (
                    ("public-css-selector-and-state-extraction", bool(css_evidence)),
                    ("live-page-dom-marker-count", bool(pages)),
                )
                if available
            ],
            "computed_style_evidence_ref": None,
        }

    return {
        "schema_version": 1,
        "audit_date": audit_date,
        "scope_note": (
            "Normative tokens and public-site component families retain exact CSS/DOM "
            "evidence only where observed. Normalized tokens and unobserved viewport/state "
            "links are explicitly marked not observed rather than borrowing generic pages."
        ),
        "source_stylesheets": stylesheet_urls,
        "token_evidence": token_index,
        "public_component_evidence": component_index,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default="docs/design-system/evidence",
        help="Directory for generated JSON evidence",
    )
    parser.add_argument("--audit-date", default=datetime.now(UTC).date().isoformat())
    parser.add_argument("--delay", type=float, default=0.12)
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    robots_data, robots_headers, robots_status, robots_final = fetch(ROBOTS_URL)
    robots_text = robots_data.decode("utf-8", "replace")
    if "Allow: /" not in robots_text:
        raise SystemExit("robots.txt does not explicitly allow public crawling")

    sitemap_urls: dict[str, list[str]] = {}
    sitemap_sources: dict[str, Any] = {}
    for locale, url in SITEMAPS.items():
        data, headers, status, final_url = fetch(url)
        urls = parse_sitemap(data)
        sitemap_urls[locale] = urls
        sitemap_sources[locale] = {
            "url": url,
            "status": status,
            "final_url": final_url,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "headers": {
                key: headers.get(key)
                for key in ("content-type", "last-modified", "etag", "date")
                if headers.get(key)
            },
            **sitemap_inventory(urls),
        }
        time.sleep(args.delay)

    page_results: list[dict[str, Any]] = []
    discovered_stylesheets: set[str] = set()
    representative_pages = select_representative_pages(sitemap_urls)
    for locale, route_signature, url in representative_pages:
        result: dict[str, Any] = {
            "locale": locale,
            "selection_reason": "first deterministic URL for normalized route signature",
            "route_signature": route_signature,
            "url": url,
        }
        try:
            data, headers, status, final_url = fetch(url)
            text = data.decode("utf-8", "replace")
            facts_parser = FactsParser()
            facts_parser.feed(text)
            facts = facts_parser.facts
            normalized_stylesheets = {
                normalize_url(href, final_url) for href in facts.stylesheets if href
            }
            stylesheets = sorted(
                url for url in normalized_stylesheets if is_allowed_source_url(url)
            )
            discovered_stylesheets.update(stylesheets)
            result.update(
                {
                    "status": status,
                    "final_url": final_url,
                    "content_type": headers.get("content-type"),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "title": facts.title,
                    "html_lang": facts.html_lang,
                    "stylesheets": stylesheets,
                    "semantic_counts": dict(facts.semantic_counts),
                    "component_hits": page_component_hits(facts),
                    "top_classes": dict(facts.classes.most_common(80)),
                }
            )
        except Exception as error:  # noqa: BLE001 - record every page audit failure
            result.update(
                {"status": "error", "error": f"{type(error).__name__}: {error}"}
            )
        page_results.append(result)
        time.sleep(args.delay)

    css_results: list[dict[str, Any]] = []
    for stylesheet in sorted(discovered_stylesheets):
        try:
            data, headers, status, final_url = fetch(stylesheet)
            text = data.decode("utf-8", "replace")
            parsed = parse_css(text, normalize_url(final_url))
            parsed.update(
                {
                    "request_url": stylesheet,
                    "status": status,
                    "headers": {
                        key: headers.get(key)
                        for key in ("content-type", "last-modified", "etag", "date")
                        if headers.get(key)
                    },
                }
            )
            css_results.append(parsed)
        except Exception as error:  # noqa: BLE001 - record every CSS audit failure
            css_results.append(
                {
                    "request_url": stylesheet,
                    "status": "error",
                    "error": f"{type(error).__name__}: {error}",
                }
            )
        time.sleep(args.delay)

    observed_base_stylesheets = {
        normalize_url(url.split("?", 1)[0]) for url in discovered_stylesheets
    }
    unexpected_stylesheets = sorted(observed_base_stylesheets - EXPECTED_STYLESHEETS)
    missing_expected_stylesheets = sorted(
        EXPECTED_STYLESHEETS - observed_base_stylesheets
    )
    page_errors = [item for item in page_results if item.get("status") == "error"]

    site_inventory = {
        "schema_version": 1,
        "audit_date": args.audit_date,
        "scope": {
            "robots_url": ROBOTS_URL,
            "robots_status": robots_status,
            "robots_final_url": robots_final,
            "robots_sha256": hashlib.sha256(robots_data).hexdigest(),
            "robots_headers": {
                key: robots_headers.get(key)
                for key in ("content-type", "last-modified", "etag", "date")
                if robots_headers.get(key)
            },
            "sitemaps": sitemap_sources,
            "total_sitemap_entries": sum(len(urls) for urls in sitemap_urls.values()),
            "total_unique_sitemap_urls": len(
                set().union(*(set(urls) for urls in sitemap_urls.values()))
            ),
            "representative_page_count": len(representative_pages),
            "normalized_route_signature_count": sum(
                len(source["normalized_route_signatures"])
                for source in sitemap_sources.values()
            ),
            "sampling_method": (
                "First deterministic URL for every locale-specific normalized route "
                "signature declared by the exhaustive sitemap inventory."
            ),
        },
        "representative_pages": page_results,
        "stylesheet_cross_check": {
            "discovered": sorted(discovered_stylesheets),
            "unexpected": unexpected_stylesheets,
            "missing_expected": missing_expected_stylesheets,
        },
        "validation": {
            "page_error_count": len(page_errors),
            "page_errors": page_errors,
            "unexpected_stylesheet_count": len(unexpected_stylesheets),
            "missing_expected_stylesheet_count": len(missing_expected_stylesheets),
        },
    }
    css_inventory = {
        "schema_version": 1,
        "audit_date": args.audit_date,
        "provenance": {
            "source": "Public Asia Allied stylesheets listed in each record",
            "purpose": "Factual token-frequency and selector traceability research",
            "excerpt_policy": (
                "bounded evidence only: no source CSS/font binary is vendored; font source URLs are omitted; "
                "each color retains at most 3 truncated selector/value examples; "
                "property distributions retain counts and the 25 most common values."
            ),
        },
        "stylesheets": css_results,
    }
    source_evidence_index = build_source_evidence_index(
        args.audit_date, page_results, css_results
    )

    (output_dir / "site-map-and-template-audit.json").write_text(
        json.dumps(site_inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "css-token-evidence.json").write_text(
        json.dumps(css_inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "source-evidence-index.json").write_text(
        json.dumps(source_evidence_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "audit_date": args.audit_date,
                "sitemap_entries": site_inventory["scope"]["total_sitemap_entries"],
                "unique_sitemap_urls": site_inventory["scope"][
                    "total_unique_sitemap_urls"
                ],
                "representative_pages": len(page_results),
                "page_errors": len(page_errors),
                "stylesheets": len(css_results),
                "token_evidence_records": len(source_evidence_index["token_evidence"]),
                "component_evidence_records": len(
                    source_evidence_index["public_component_evidence"]
                ),
                "unexpected_stylesheets": unexpected_stylesheets,
                "missing_expected_stylesheets": missing_expected_stylesheets,
                "output_dir": str(output_dir),
            },
            indent=2,
        )
    )
    return (
        1
        if page_errors or unexpected_stylesheets or missing_expected_stylesheets
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
