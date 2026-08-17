# Asia Allied-derived visual baseline

## Purpose

This reference explains where the scaffold's visual baseline came from and how agents may use it. Root `DESIGN.md` remains normative for exact tokens and component contracts.

The baseline is evidence-based and accessibility-corrected. It is not an official corporate brand manual and does not grant permission to reuse trademarks, logos, photographs, copy, fonts or compiled website assets.

## Audit scope

Audit date: 2026-08-14.

- Target: `https://www.asiaalliedgroup.com/en`
- Published sitemap records parsed and classified: 10,669
- Unique published URLs: 10,666
- Locale totals: English 3,771; Traditional Chinese 2,879; Simplified Chinese 4,019
- Deterministic representative pages fetched: 100
- Locale-specific normalized route signatures: 579; these were not all individually rendered
- Parsed public stylesheet rules: 2,883

The audit does not claim that every published content URL was fetched. Reproducible commands, bounded evidence, hashes and failure records are in `docs/design-system/source-audit.md` and `docs/design-system/evidence/`.

## Four evidence classes

Keep these classes separate in documentation and implementation:

1. **Observed public-site values** — declarations, computed styles and patterns directly observed on representative public pages.
2. **Official artwork samples** — colors sampled from publicly served logo artwork.
3. **Normalized product-system decisions** — deliberately regularized scales for company applications.
4. **Accessibility corrections** — semantic values changed to meet product accessibility requirements.

For example, the accessible orange product token is not evidence that the live site's ordinary orange button background uses that value.

## Usage boundaries

Allowed:

- use root `DESIGN.md` and generated artifacts as the company scaffold's implementation baseline;
- use the Admin CMS HTML template as an information-density and composition reference;
- create distinct layouts for public, field, campaign and showcase products while retaining shared visual DNA;
- rerun the bounded audit when the public stylesheet changes and review the resulting diff.

Not allowed:

- copy the complete compiled public stylesheet, logo binaries, fonts, photographs or page content into a product;
- claim the baseline is an official internal brand manual;
- claim exhaustive rendering of all published URLs;
- hotlink production UI to public-site assets;
- publish credentials, private hosts, local paths or internal URLs in evidence or templates.

## Typography and licensing

The audited site referenced Pragati Narrow and Roboto. Current Google Fonts distributions for both are under OFL-1.1. Production applications must load approved font files through the approved asset pipeline and retain required licence notices. The static HTML template remains dependency-free and therefore uses system fallbacks when these fonts are not installed.

Traditional Chinese interfaces must include the CJK fallback stack specified in root `DESIGN.md` and must be tested with realistic long labels and table content.

## Icon policy

- New React/Vite products: Lucide
- Bootstrap-standardized products: Bootstrap Icons
- Broad catalogue or brand coverage: Font Awesome Free, with its split licences and trademark restrictions reviewed
- Do not establish `react-icons` as a company-wide standard

## Change control

When `DESIGN.md` changes:

1. regenerate all artifacts using `scripts/export_design_system.py`;
2. run the exporter drift check and DTCG schema validation;
3. update the Admin HTML reference only when its semantic tokens or component contract changed;
4. run skill/template parity tests and responsive visual review;
5. document whether each change is new evidence, normalization or accessibility correction.
