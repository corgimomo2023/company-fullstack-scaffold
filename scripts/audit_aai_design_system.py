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
COMPONENT_MARKERS = {
    "site-header": ("header", "main-menu", "header__"),
    "site-search": ("sitesearch", "site-search"),
    "breadcrumbs": ("breadcrumb",),
    "hero-carousel": ("key-visual", "slick-slider"),
    "content-card": ("img-title-blk", "img-card-blk", "top-img-blk"),
    "image-overlay-card": ("img-overlay-blk", "overlay-cover-blk"),
    "image-plate": ("img-plate-blk", "img-space-plate-blk"),
    "listing-table": ("listing-table",),
    "year-accordion": ("rte-year-collapse", "history-year-blk"),
    "tag-filter": ("tag-list", "tag.selected"),
    "pagination": ("pagination", "pager"),
    "form-control": ("form-control", "field__", "checkbox-input", "radio-input"),
    "select-control": ("js-selectBox", "multiselect-container"),
    "button": ("btn",),
    "social-links": ("soc-sq", "social"),
    "back-to-top": ("bk2Top",),
    "footer": ("footer", "contact-bottom"),
    "rich-text": ("rte",),
    "video-link": ("video-link",),
    "global-footprint-map": ("f-map",),
    "document-download": ("download", "report"),
}

HEX_RE = re.compile(
    r"(?<![\w-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})(?![0-9a-fA-F])"
)
RGB_RE = re.compile(r"rgba?\([^)]*\)", re.IGNORECASE)
COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
MEDIA_RE = re.compile(r"@media\s*\(([^)]*)\)", re.IGNORECASE)
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


def fetch(url: str, *, retries: int = 3) -> tuple[bytes, dict[str, str], int, str]:
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
            with urllib.request.urlopen(request, timeout=30) as response:
                return (
                    response.read(),
                    {k.lower(): v for k, v in response.headers.items()},
                    response.status,
                    response.geturl(),
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
        signature_parts: list[str] = []
        for part in parts:
            if re.fullmatch(r"(?:19|20)\d{2}", part):
                signature_parts.append("{year}")
            elif re.fullmatch(r"page\d+", part):
                signature_parts.append("{page}")
            elif part == parts[-1] and len(parts) >= 2:
                signature_parts.append("{slug}")
            else:
                signature_parts.append(part)
        signatures["/".join(signature_parts) or "home"] += 1
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
        "template_signatures": dict(sorted(signatures.items())),
    }


def select_representative_pages(
    sitemaps: dict[str, list[str]],
) -> list[tuple[str, str, str]]:
    selected: list[tuple[str, str, str]] = []
    seen_normalized_signatures: set[tuple[str, str, int]] = set()
    for locale, urls in sitemaps.items():
        for url in sorted(set(urls)):
            parts = locale_neutral_parts(url)
            category = parts[0] if parts else "home"
            depth = len(parts)
            # Sample every locale independently. Shared CSS does not imply that
            # translated templates have identical markup or language metadata.
            signature = (locale, category, depth)
            if signature in seen_normalized_signatures:
                continue
            seen_normalized_signatures.add(signature)
            selected.append((locale, f"{category}:depth-{depth}", url))
    # Explicitly cross-check high-value templates in every language.
    for locale, prefix in (("en", ""), ("tc", "/tc"), ("sc", "/sc")):
        for label, suffix in (
            ("home", "/"),
            ("about", "/the-group/about-the-group"),
            ("projects", "/projects"),
            ("investor-reports", "/investor-relations/financial-reports"),
            ("career", "/career"),
            ("contact", "/contact-us"),
        ):
            url = f"{BASE_URL}{prefix}{suffix}".replace("//", "/").replace(
                "https:/", "https://"
            )
            if not any(existing_url == url for _, _, existing_url in selected):
                selected.append((locale, f"explicit:{label}", url))
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
        )
    }
    clean = COMMENT_RE.sub("", css)
    rules = 0
    for match in RULE_RE.finditer(clean):
        selector = " ".join(match.group(1).split())
        if selector.startswith("@"):
            continue
        rules += 1
        for raw_decl in match.group(2).split(";"):
            if ":" not in raw_decl:
                continue
            prop, value = raw_decl.split(":", 1)
            prop = prop.strip().lower()
            value = value.strip()
            if prop in property_values:
                property_values[prop][value] += 1
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
            }
            for prop, counter in property_values.items()
        },
        "media_queries": dict(collections.Counter(MEDIA_RE.findall(css)).most_common()),
        "component_selector_hits": {
            component: sum(css.count(marker) for marker in markers)
            for component, markers in COMPONENT_MARKERS.items()
        },
    }


def page_component_hits(facts: PageFacts) -> dict[str, int]:
    haystack = " ".join((*facts.classes.keys(), *facts.ids.keys()))
    return {
        component: sum(haystack.count(marker) for marker in markers)
        for component, markers in COMPONENT_MARKERS.items()
        if any(marker in haystack for marker in markers)
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
    for locale, reason, url in representative_pages:
        result: dict[str, Any] = {
            "locale": locale,
            "selection_reason": reason,
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
            "sampling_method": (
                "First deterministic URL in every locale/category/depth stratum plus "
                "explicit home, about, projects, investor reports, career and contact pages."
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
                "No source CSS/font binary is vendored; font source URLs are omitted; "
                "each color retains at most 3 truncated selector/value examples; "
                "property distributions retain counts and the 25 most common values."
            ),
        },
        "stylesheets": css_results,
    }

    (output_dir / "site-map-and-template-audit.json").write_text(
        json.dumps(site_inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "css-token-evidence.json").write_text(
        json.dumps(css_inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
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
