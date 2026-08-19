"""Rebuild CSS/token/component evidence from a completed page-signature audit.

Use this when DESIGN.md evidence mapping or CSS parsers change after the expensive
page crawl. It reuses recorded live page/template results and refetches only the
small set of discovered public stylesheets.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from audit_aai_design_system import (
    build_source_evidence_index,
    fetch,
    is_allowed_source_url,
    normalize_url,
    parse_css,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_dir", type=Path)
    parser.add_argument("--target-dir", type=Path)
    parser.add_argument("--audit-date", default="2026-08-19")
    args = parser.parse_args()

    site_path = args.audit_dir / "site-map-and-template-audit.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    pages = site["representative_pages"]

    stylesheets = []
    for url in site["stylesheet_cross_check"]["discovered"]:
        if not is_allowed_source_url(url):
            raise ValueError(f"Refusing out-of-scope stylesheet URL: {url}")
        data, headers, status, final_url = fetch(url)
        parsed = parse_css(data.decode("utf-8", "replace"), normalize_url(final_url))
        parsed.update(
            {
                "request_url": url,
                "status": status,
                "headers": {
                    key: headers.get(key)
                    for key in ("content-type", "last-modified", "etag", "date")
                    if headers.get(key)
                },
            }
        )
        stylesheets.append(parsed)

    css_inventory = {
        "schema_version": 2,
        "audit_date": args.audit_date,
        "provenance": {
            "source": "Public Asia Allied stylesheets listed in each record",
            "purpose": (
                "Factual token-frequency, declaration and selector traceability research"
            ),
            "excerpt_policy": (
                "No source CSS/font binary is vendored; font source URLs are omitted; "
                "selector/value excerpts are bounded."
            ),
        },
        "stylesheets": stylesheets,
    }
    evidence_index = build_source_evidence_index(args.audit_date, pages, stylesheets)

    css_path = args.audit_dir / "css-token-evidence.json"
    index_path = args.audit_dir / "source-evidence-index.json"
    css_path.write_text(
        json.dumps(css_inventory, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    index_path.write_text(
        json.dumps(evidence_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.target_dir:
        args.target_dir.mkdir(parents=True, exist_ok=True)
        for path in (site_path, css_path, index_path):
            shutil.copy2(path, args.target_dir / path.name)

    print(
        json.dumps(
            {
                "page_signatures": len(pages),
                "stylesheets": len(stylesheets),
                "token_evidence_records": len(evidence_index["token_evidence"]),
                "component_evidence_records": len(
                    evidence_index["public_component_evidence"]
                ),
                "target_dir": str(args.target_dir) if args.target_dir else None,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
