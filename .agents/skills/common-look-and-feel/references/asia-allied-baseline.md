# Asia Allied-derived visual baseline

## Purpose

This reference explains where the scaffold's visual baseline came from and how agents may use it. Root `DESIGN.md` remains normative for exact tokens and component contracts. The clickable evidence register is `docs/design-system/source-evidence.md`.

The baseline is evidence-based and accessibility-corrected. It is not an official corporate brand manual and does not grant permission to reuse trademarks, logos, photographs, copy, fonts or compiled website assets.

## Audit scope

Audit date: 2026-08-19.

Coverage is reported in separate layers:

1. **Discovery:** 10,669 sitemap entries and 10,666 unique published URLs across English, Traditional Chinese and Simplified Chinese.
2. **Normalized route HTTP coverage:** 559 locale-specific route signatures — English 188, Traditional Chinese 175 and Simplified Chinese 196 — with one deterministic live request per signature. Within an explicit content/archive-root allowlist, years, months, numeric IDs, pagination and true content-detail slugs are abstracted; all unclassified sibling routes and functionally distinct IR, group and business-sector static pages stay separate.
3. **Responsive route/content coverage:** 43 profiles rendered at desktop, tablet and mobile widths: 31 detailed English profiles plus six high-value Traditional Chinese and six Simplified Chinese profiles covering home, group static, investor reports, publication listing, project listing and contact/form routes.
4. **Source evidence:** 62 token records and 52 public component-family records generated from exact CSS declarations/media queries and route-specific DOM markers. Responsive computed styles are a separate profile-level artifact; they are not attached to every token/component without a specific result/probe link.

Neither 559 nor 43 is a count of independently authored website templates. The audit does not claim that every one of the 10,666 unique content URLs was individually fetched in a browser or visually inspected. Complete inventories, bounded evidence, hashes, failures and reproduction commands are in `docs/design-system/source-audit.md` and `docs/design-system/evidence/`.

## Four evidence classes

Keep these classes separate in documentation and implementation:

1. **Observed public-site values** — declarations, computed styles and patterns directly observed on public pages.
2. **Cross-page patterns** — repeated source behavior supported by multiple pages/selectors.
3. **Normalized product-system decisions** — deliberately regularized scales and component contracts for company applications.
4. **Accessibility corrections** — semantic values or behavior changed to meet product accessibility requirements.

Logo colors are separately recorded as official-artwork samples. They are evidence from publicly served artwork, not general-purpose status/control colors.

For example, `text-on-accent: #001C19` and the accessible orange product token are scaffold accessibility decisions. They are not claims that the live website names or consistently uses those tokens.

## Evidence lookup contract

Before changing or challenging a token/component:

1. open its row in `docs/design-system/source-evidence.md`;
2. inspect the exact source CSS declaration/media query, or open the primary live URL and route/DOM location when one is linked;
3. inspect a stated viewport/state only when a specific computed result/probe is linked;
4. review cross-check URLs and evidence method;
5. preserve the observed/normalized/accessibility classification;
6. write `not observed` when the public site did not expose a state — never invent live evidence from a scaffold contract.

## Usage boundaries

Allowed:

- use root `DESIGN.md` and generated artifacts as the company scaffold's implementation baseline;
- use the Admin CMS HTML template as an information-density and composition reference;
- create distinct layouts for public, field, campaign and showcase products while retaining shared visual DNA;
- rerun the bounded audit when the public stylesheet/sitemap changes and review the resulting diff.

Not allowed:

- copy the complete compiled public stylesheet, logo binaries, fonts, photographs or page content into a product;
- claim the baseline is an official internal brand manual;
- describe route signatures or responsive profiles as exhaustive independent template coverage;
- claim exhaustive browser rendering of all published URLs;
- hotlink production UI to public-site assets;
- publish credentials, private hosts, local paths or internal URLs in evidence or templates.

## Typography and licensing

The audited site referenced Pragati Narrow and Roboto. Current Google Fonts distributions for both are under OFL-1.1. Production applications must load approved font files through the approved asset pipeline and retain required licence notices. The static HTML template remains dependency-free and therefore uses system fallbacks when these fonts are not installed.

Traditional and Simplified Chinese interfaces use the generated CJK fallback stack (`Noto Sans TC`, `Microsoft JhengHei`, then system sans fallbacks) and must be tested with realistic long labels, headings, forms and table content.

## Icon policy

- New React/Vite products: Lucide
- Bootstrap-standardized products: Bootstrap Icons
- Broad catalogue or brand coverage: Font Awesome Free, with its split licences and trademark restrictions reviewed
- Do not establish `react-icons` as a company-wide standard

## Change control

When `DESIGN.md` changes:

1. regenerate all six artifacts using `scripts/export_design_system.py`;
2. run exporter drift and DTCG schema validation;
3. rebuild/render evidence when source mappings change;
4. update the Admin HTML reference only when its semantic tokens or component contract changed;
5. run skill/template parity tests, frontend checks and responsive rendering;
6. document whether each change is observed evidence, a cross-page pattern, normalization or accessibility correction.
