# Asia Allied public-site source audit

Audit date: **2026-08-19**

This document records how the evidence behind [`DESIGN.md`](../../DESIGN.md) was produced. It deliberately separates URL discovery, normalized route HTTP coverage, responsive browser profiles and token/component mapping. None of those layers is an independent-template count. This audit does **not** claim that every content URL was individually fetched in a browser or visually inspected.

## Public sources

| Source | Purpose |
|---|---|
| <https://www.asiaalliedgroup.com/robots.txt> | Crawl permission and sitemap discovery |
| <https://www.asiaalliedgroup.com/sitemap.xml> | English/public-default URL inventory |
| <https://www.asiaalliedgroup.com/sitemap-tc.xml> | Traditional Chinese URL inventory |
| <https://www.asiaalliedgroup.com/sitemap-sc.xml> | Simplified Chinese URL inventory |
| <https://www.asiaalliedgroup.com/assets/css/projectbase.css> | Screen typography, palette, layout, components and responsive rules |
| <https://www.asiaalliedgroup.com/assets/css/print.css> | Print overrides and bundled shared foundations |
| rendered live pages listed in [`source-evidence.md`](source-evidence.md) | DOM, computed-style, state and responsive cross-checks |

`robots.txt` returned HTTP 200 and explicitly allowed `/`. The route audit uses exact HTTPS-origin checks, a named user agent, bounded retries and a delay between requests.

### Provenance and publication boundary

Asia Allied remains the source owner for its CSS, fonts, marks, imagery and content. This repository does not vendor or relicense those files. Machine evidence stores hashes, counts, bounded selector/value excerpts and DOM facts; it is not sufficient to reconstruct the source stylesheet. Brand marks and fonts still require corporate and licence approval before production use.

## Coverage model

### 1. Exhaustive sitemap discovery

Every `<loc>` entry in all three published sitemaps was parsed and classified by locale, category, path depth and normalized route signature.

| Locale | Entries | Unique | Duplicate entries | Sitemap last-modified |
|---|---:|---:|---:|---|
| English/default | 3,771 | 3,770 | 1 | 2026-08-18 16:05:06 GMT |
| Traditional Chinese | 2,879 | 2,878 | 1 | 2022-10-17 16:15:03 GMT |
| Simplified Chinese | 4,019 | 4,018 | 1 | 2026-08-18 16:20:05 GMT |
| **Total** | **10,669** | **10,666** | **3** | — |

Each sitemap contains one duplicate entry. No out-of-scope host or non-HTTPS sitemap entry was found. The Traditional Chinese sitemap is materially older than the others; content parity must not be inferred from counts.

The full URL/signature inventory is in [`evidence/site-map-and-template-audit.json`](evidence/site-map-and-template-audit.json). The historical filename is retained for compatibility; its machine field is `normalized_route_signatures`, not `template_signatures`.

### 2. Locale-specific normalized route HTTP coverage

The audit selects one deterministic live URL for every **locale + normalized route signature**. Dynamic abstraction is applied only inside an explicit content/archive-root allowlist (`blog`, `career`, director detail, `enews`, press-release and media-coverage families). Unclassified sibling routes remain literal. The normalization rules are intentionally narrow:

- abstract publication years as `{year}`;
- abstract blog archive months as `{month}`;
- abstract `pageN` pagination as `{page}`;
- abstract final numeric content IDs as `{id}`;
- abstract true content-detail slugs as `{slug}`;
- preserve functionally distinct Investor Relations, Group and project-sector static paths verbatim.

Examples that remain separate include:

- `investor-relations/financial-reports`;
- `investor-relations/corporate-governance`;
- `investor-relations/stock-chart`;
- `investor-relations/ir-calendar`;
- `projects/construction`;
- `projects/professional-services`;
- `the-group/about-the-group`;
- `the-group/vision-mission-and-core-values`.

Examples deliberately consolidated include `blog/01/...` through `blog/12/...` as `blog/{month}/...`, year archives, pagination and repeated article/job instances.

| Locale | Normalized route signatures |
|---|---:|
| English | 188 |
| Traditional Chinese | 175 |
| Simplified Chinese | 196 |
| **Total** | **559** |

Final HTTP result: **559/559 responses returned status 200, with 0 request/parser errors**. MIME distribution was 552 HTML, three PDF, three JPEG and one XML response. Final URLs, redirects, hashes and content types are retained in the artifact. Every request target, sitemap URL and redirect hop is rejected unless it remains on the exact `https://www.asiaalliedgroup.com` origin.

A route signature is a coverage unit, not proof of an independently authored template. Some sitemap signatures resolve to PDF, image or XML responses rather than HTML; MIME type, final URL, redirect and hash are retained so they are not mislabeled as rendered pages.

### 3. Responsive computed-style coverage

The Playwright collector renders **43 route/content profiles** at all three viewports:

- desktop: 1440×900;
- tablet: 768×900;
- mobile: 390×844.

Profile composition:

- 31 detailed English profiles, including every Investor Relations static destination, every project-sector landing page and major home/group/list/detail/job/form/legal patterns;
- six Traditional Chinese profiles: home, group about, investor reports, publication list, project list and contact form;
- six Simplified Chinese profiles covering the same high-value families.

Final schema-v2 browser result: **129/129 profile/viewport records returned status 200, with 0 collector failures and 0 measured horizontal-overflow cases**. Locale distribution was 93 English, 18 Traditional Chinese and 18 Simplified Chinese records. The artifact contains 1,022 visible default-style samples and 255 successful state samples: button hover/focus/pointer-active 56 each, card hover 21, card focus 3, input focus 33, tag hover 9, tag selected 3 and active tab 18. No visible disabled button/input sample was found, so disabled remains `not observed`; missing probes are omitted rather than counted as null records. A successful profile/viewport record proves route rendering and only its non-null samples, not every named function or component on that route.

The browser request router allows only the exact `https://www.asiaalliedgroup.com` origin plus `data:`/`blob:` resources. Cross-origin redirects and subresources are blocked. The collector records response status, final URL, page title, HTML hash, body/document widths, horizontal-overflow result, visible selector samples and successfully applied/observed states. Hover, focus and pointer-active probes require a visible enabled element; disabled, selected and active-class probes are static observations. A missing live state is `not observed`; normalized product behavior is not rewritten as live-site evidence.

### 4. Token and component mapping

The generated evidence index contains:

- 62 token records;
- 52 public component-family records;
- 31 normalized scaffold visual variants;
- product behavior contracts with per-variant/state `mapped` or `behavior-only` coverage.

Each record carries only evidence actually available: exact CSS declarations/media queries, concrete route/DOM-marker locations, CSS state selectors, and source URLs. `viewport_scope` and `computed_style_evidence_ref` remain empty unless a record is linked to a specific computed result; this audit does not borrow generic English pages or all three viewports for every token/component. Normalized tokens without an exact declaration are explicitly `not-observed`.

Of the 62 token records, 44 retain an exact raw CSS declaration or media-query match and 18 have no exact source match. Even when a raw value matches, its semantic token name remains classified as normalized; `accent-accessible` and `text-on-accent` remain explicit accessibility corrections.

The human-readable version is [`source-evidence.md`](source-evidence.md). For normalized visual variants, a linked public pattern does not imply the exact product state appeared in rendered DOM; the register distinguishes public DOM patterns, CSS-only state selectors and `not observed as live state`.

## Stylesheet integrity

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `projectbase.css` | 454,544 | `ff62bae815e73cb956e935b15bb4df7bec36e6c8013c38bd69a8bc7ab3f5dc94` |
| `print.css` | 256,301 | `b99d6336f7da208f0d859a30cdbd0fb3e2cb1cff138732013a208751d9ae2e98` |

The screen stylesheet yielded 2,883 parsed rules. Evidence stores complete extracted declaration counts/property distributions and bounded examples, not a reusable copy. The live stylesheet hash matched the prior recorded source during this audit; the coverage defects were in the former audit model/documentation, not evidence of a sudden CSS change.

## Observed values versus product normalization

Keep these categories separate:

1. **Observed raw value** — directly found in source CSS, artwork or computed style.
2. **Cross-page pattern** — repeated across selectors/pages.
3. **Normalized scaffold token/component** — an internal production contract derived from the pattern.
4. **Accessibility correction** — deliberately changed foreground, sizing, focus or behavior.

Examples:

- observed accent orange: `#E6762D`;
- white on that orange: about 3.00:1, unsuitable for normal text;
- normalized `text-on-accent`: `#001C19`, about 5.93:1 on the orange;
- `text-on-accent` is a scaffold accessibility token, not a claimed Asia Allied token name;
- source controls around 35.6px are raised to a 44px product minimum;
- source Bootstrap-blue focus is replaced by the scaffold's visible green focus treatment.

## Reproduction

```bash
backend/.venv/bin/python scripts/audit_aai_design_system.py \
  --audit-date 2026-08-19 \
  --output-dir docs/design-system/evidence

node scripts/audit_aai_computed_styles.mjs \
  docs/design-system/evidence/computed-style-walkthrough.json

backend/.venv/bin/python scripts/export_design_system.py
backend/.venv/bin/python scripts/render_design_evidence.py

npx -y @google/design.md@0.4.0 lint DESIGN.md
backend/.venv/bin/python scripts/export_design_system.py --check
backend/.venv/bin/python scripts/render_design_evidence.py --check
```

Re-run the live audit when a sitemap or stylesheet hash changes. Review diffs; never blindly replace normalized/accessibility-corrected product tokens with literal source values.
