# Asia Allied public-site source audit

Audit date: **2026-08-14**

This document records how the design-system evidence in [`DESIGN.md`](../../DESIGN.md) was produced. It separates exhaustive sitemap analysis from bounded page fetching so that coverage claims remain precise.

## Public sources

| Source | Purpose |
|---|---|
| <https://www.asiaalliedgroup.com/robots.txt> | Crawl permission and sitemap discovery |
| <https://www.asiaalliedgroup.com/sitemap.xml> | English/public-default URL inventory |
| <https://www.asiaalliedgroup.com/sitemap-tc.xml> | Traditional Chinese URL inventory |
| <https://www.asiaalliedgroup.com/sitemap-sc.xml> | Simplified Chinese URL inventory |
| `assets/css/projectbase.css` | Screen typography, palette, layout, components and responsive rules |
| `assets/css/print.css` | Print overrides and shared bundled foundations |
| `assets/img/main-logo-1x.png` | Main-logo palette cross-check |
| rendered pages at 375px and 1440px | Computed style and responsive cross-check |

`robots.txt` returned HTTP 200 and explicitly allowed `/`. The audit uses a named user agent, retries transient failures and a small delay between representative page requests.

### Provenance and publication boundary

Asia Allied remains the source owner for its site CSS, fonts, marks, imagery and content. This public repository does not vendor those files or relicense them. The machine-readable CSS evidence is a factual research extract limited to hashes, aggregate counts, at most three truncated selector/value examples per color, font family/weight/style metadata without source URLs, and the 25 most common values per audited property. It is not sufficient to reconstruct the source stylesheet. Brand marks and fonts still require corporate and licence approval before production use.

## Exhaustive sitemap inventory

Every `<loc>` entry in all three sitemaps was parsed and classified by locale, top-level category, path depth and normalized route signature.

| Locale | Entries | Unique | Duplicate entries | Sitemap last-modified |
|---|---:|---:|---:|---|
| English/default | 3,771 | 3,770 | 1 | 2026-08-13 16:05:06 GMT |
| Traditional Chinese | 2,879 | 2,878 | 1 | 2022-10-17 16:15:03 GMT |
| Simplified Chinese | 4,019 | 4,018 | 1 | 2026-08-13 16:20:06 GMT |
| **Total** | **10,669** | **10,666** | **3** | — |

No out-of-scope host or non-HTTPS sitemap entries were found. Each sitemap duplicated its locale homepage once. The Traditional Chinese sitemap has a materially older `Last-Modified` header than the English and Simplified Chinese versions; do not infer content parity from sitemap counts.

### Category counts

| Category | EN | TC | SC |
|---|---:|---:|---:|
| Blog and tag/year/page routes | 3,551 | 2,693 | 3,799 |
| Press releases | 102 | 82 | 102 |
| Careers | 30 | 26 | 30 |
| E-news | 29 | 19 | 29 |
| Media coverage | 16 | 17 | 16 |
| Directors/board members | 12 | 12 | 12 |
| Investor relations | 11 | 11 | 11 |
| Projects | 7 | 6 | 7 |
| Group pages | 3 | 3 | 3 |
| Other static pages | 10 | 10 | 10 |

The complete URL-signature inventory is machine-readable in [`evidence/site-map-and-template-audit.json`](evidence/site-map-and-template-audit.json). It intentionally records counts and signatures rather than copying the site's content.

## Representative page fetching

The sitemap inventory is exhaustive; HTTP page fetching is stratified rather than exhaustive. The script selects the first deterministic URL for every **locale + top-level category + path depth** stratum, then adds explicit home, about, projects, financial reports, career and contact pages for every language.

Results:

- 100 representative requests;
- 100 successful HTTP responses;
- 0 request/parser errors;
- every locale sampled independently;
- only `projectbase.css` and `print.css` discovered as same-origin stylesheets across the sample set;
- 15 redirects observed, including group/news aliases and three locale variants of a press-release URL that resolve to the same PDF document.

This method verifies every locale/category/depth stratum without downloading all 10,669 entries. It does **not** prove every one of the 579 locale-specific normalized signature records has a distinct DOM template, and it does **not** claim that every content URL was individually fetched or visually inspected. Page-template families in the component inventory combine sampled DOM evidence, shared stylesheet selectors and sitemap inference; they are labelled accordingly.

## Stylesheet integrity

| Asset | Bytes | SHA-256 | Server last-modified |
|---|---:|---|---|
| `projectbase.css` | 454,544 | `ff62bae815e73cb956e935b15bb4df7bec36e6c8013c38bd69a8bc7ab3f5dc94` | 2026-08-14 07:09:46 GMT |
| `print.css` | 256,301 | `b99d6336f7da208f0d859a30cdbd0fb3e2cb1cff138732013a208751d9ae2e98` | 2023-02-21 08:08:50 GMT |

The screen stylesheet yielded 2,883 parsed CSS rules. The evidence JSON stores complete extracted-color declaration counts/property distributions and a bounded set of selector/value examples. It is a traceability extract, not a copy of the stylesheet. This prevents bundled Bootstrap defaults from being mistaken for brand colors while keeping the third-party excerpt limited.

## Logo integrity and palette

| Asset | Dimensions | SHA-256 | Dominant opaque colors |
|---|---:|---|---|
| `main-logo-1x.png` | 422×46 | `3d416329cccb7610860b26eb8d39d7dc9d5eab34677a654f81e51840c67a3566` | `#231F20`, `#F7941D`, `#7B7A1B` |
| `sub-logo-1x.png` | 191×46 | `b4652a8212cddd0bb6acfd803ed3a9e73c072dc985e98d9725751327cbc29179` | `#F49233`, `#7C7835` plus raster antialiasing |

The source PNG files are not copied into this repository. The sampled values are factual evidence only; brand marks still require an approved asset and trademark/brand review.

## Responsive computed-style cross-check

The About page was inspected at 1440×900 and 375×812:

- body: Roboto 400, 16.016px, `#333333`;
- page H1: Pragati Narrow 700, 50.05px desktop / 25.025px mobile, `#006A63`;
- content H2: Roboto 700, 24.024px desktop / 17.017px mobile;
- content paragraph: Roboto 400, 18.018px/28.028px desktop and 14.014px/21.8px mobile;
- breadcrumb: 14.014px desktop and hidden at the sampled mobile state;
- container: 15px side padding and 1570px maximum width;
- header: white desktop, `#ECECEC` mobile;
- footer: `#CECECE` background.

These computed values cross-check the compiled CSS cascade. The normative product typography deliberately normalizes the unusual 16.016px root and tight base line-height rather than reproducing them literally.

## Reproduction

```bash
python3 scripts/audit_aai_design_system.py --audit-date YYYY-MM-DD
npx -y @google/design.md@0.4.0 lint DESIGN.md
python3 scripts/export_design_system.py
python3 scripts/export_design_system.py --check

curl -fsSL https://www.designtokens.org/schemas/2025.10/format.json \
  -o /tmp/dtcg-format-schema.json
npx -y ajv-cli@5 validate --spec=draft7 --strict=false --all-errors \
  -s /tmp/dtcg-format-schema.json -d design-system/tokens.json
```

Re-run the audit when a sitemap, stylesheet hash or main-logo hash changes. Review diffs rather than blindly replacing normative accessible tokens with literal source values.
