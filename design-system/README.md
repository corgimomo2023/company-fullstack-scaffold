# Design-system artifacts

[`../DESIGN.md`](../DESIGN.md) is the normative source. The files in this directory are generated; do not edit them by hand.

| Artifact | Consumer | Contract coverage |
|---|---|---|
| [`theme.css`](theme.css) | Tailwind CSS v4 `@theme` import | Foundation tokens, complete font stacks, line heights, breakpoints, containers, elevation and motion |
| [`foundation.css`](foundation.css) | Framework-neutral CSS/runtime import | CSS custom properties plus complete `.type-*` typography utilities |
| [`tailwind.theme.json`](tailwind.theme.json) | Tailwind CSS v3 `theme.extend` mapping | Foundations, responsive tokens, font stacks and composite font-size/line-height settings |
| [`tailwind.preset.cjs`](tailwind.preset.cjs) | Tailwind CSS v3 preset consumers | Generated CommonJS wrapper around the Tailwind contract |
| [`tokens.json`](tokens.json) | DTCG Format Module 2025.10 consumers | Foundations and typography; component/evidence contracts in a namespaced `$extensions` record |
| [`components.json`](components.json) | Framework-neutral component tooling | 31 visual records, behavior contracts, evidence and per-variant/state implementation coverage |
| [`asia-allied-design-system.pen`](asia-allied-design-system.pen) | pen.dev canvas | Complete 20-board visual derivative: foundations, every visual/behavior contract, responsive examples, evidence, coverage and guidance; not a normative source |

## Why a wrapper is required

`@google/design.md@0.4.0` is the pinned parser/exporter, but its raw exports omit typography `lineHeight`, produce DTCG `letterSpacing` values in an unsupported `em` unit and do not carry the complete component/evidence contract. [`scripts/export_design_system.py`](../scripts/export_design_system.py) enriches those outputs deterministically.

The wrapper also makes implementation completeness explicit. Every behavior `variant × state` is marked either:

- `mapped`: backed by a named visual component record; or
- `behavior-only`: required behavior that a consumer must style and verify, without pretending a visual mapping already exists.

## Regenerate and validate

```bash
pip install -r requirements-design.txt
npx -y @google/design.md@0.4.0 lint DESIGN.md
python3 scripts/export_design_system.py
python3 scripts/export_design_system.py --check
python3 scripts/export_pen_design_system.py
python3 scripts/export_pen_design_system.py --check

curl -fsSL https://www.designtokens.org/schemas/2025.10/format.json \
  -o /tmp/dtcg-format-schema.json
npx -y ajv-cli@5 validate --spec=draft7 --strict=false --all-errors \
  -s /tmp/dtcg-format-schema.json -d design-system/tokens.json
```

CI runs the same drift and official-schema checks.

## pen.dev visual board

The `.pen` file is generated from `DESIGN.md`, `tokens.json` and `components.json`; the JSON artifacts are themselves generated from `DESIGN.md`. This one-way flow prevents the canvas from becoming a second, drifting source of truth. The committed preview is [`../docs/design-system/asia-allied-design-system.png`](../docs/design-system/asia-allied-design-system.png).

The cover metadata records exporter version `3`, the audit date, validated pen.dev CLI version and deterministic SHA-256 hashes of all three inputs. This provides reproducible provenance without embedding timestamps or commit IDs that would make every regeneration drift.

The catalogue contains **20 separated boards** arranged by category:

1. cover, manifest and governance;
2. all 20 color tokens with semantic role, evidence classification and usage boundary;
3. eight normative contrast pairs and color-accessibility rules;
4. all 10 typography roles including size, weight, line height and tracking;
5. English/CJK/long-copy localization specimens and font governance;
6. all 10 spacing tokens, four radii, six breakpoints, five containers and layout rules;
7. two elevations, five motion tokens and shape rules;
8. two visual-contract boards covering all 31 generated visual records;
9. four behavior-contract boards covering all 31 components without truncating variants, states or requirements;
10. the complete 345-cell variant/state implementation matrix;
11. the complete 101-item requirement register plus icons, imagery and licensing boundaries;
12. desktop, tablet and mobile compositions;
13. 11 summarized page-pattern/adaptation families, explicitly not an authored-template count;
14. five evidence/provenance classifications;
15. sitemap, HTTP, browser and implementation coverage limitations; and
16. all normative do/don't guidance.

The implementation coverage board deliberately distinguishes the 48 mapped variant-state records from 297 `behavior-only` records. A behavior contract shown in the catalogue is not presented as an already implemented production component.

With the official pen.dev CLI installed, validate the file through the actual editor engine and refresh the preview:

```bash
npm install -g @pen.dev/cli
pen --in design-system/asia-allied-design-system.pen \
  --export docs/design-system/asia-allied-design-system.png \
  --export-scale 1
```

## Tailwind v4

Import the generated theme after Tailwind:

```css
@import "tailwindcss";
@import "../../design-system/theme.css";
```

This exposes utilities such as `bg-primary`, `text-accent-accessible`, `rounded-md`, `p-lg` and `text-body-md`. Every generated font role contains approved Latin/CJK/system fallbacks rather than one comma-separated family masquerading as a single font.

## Tailwind v3

Use `tailwind.preset.cjs`, or merge `tailwind.theme.json` under the application's existing configuration. Preserve unrelated content/plugin settings. Every named `fontSize` entry retains its normative line height and every `fontFamily` entry retains the full fallback array.

## Framework-neutral/runtime use

Import `foundation.css` before application styles:

```css
@import "../../design-system/foundation.css";
```

Use CSS custom properties for semantic values. The generated `.type-*` classes apply family, size, weight, line height and tracking together so consumers do not accidentally implement partial typography tokens.

`tokens.json` validates against its declared DTCG 2025.10 schema. DTCG has no standard component-contract type, so components and evidence live under the `com.github.corgimomo2023.company-fullstack-scaffold` extension. Consumers without extension support can read `components.json`.

## Evidence and ownership

- Clickable token/component register: [`../docs/design-system/source-evidence.md`](../docs/design-system/source-evidence.md)
- Research method and source integrity: [`../docs/design-system/source-audit.md`](../docs/design-system/source-audit.md)
- Components and page patterns: [`../docs/design-system/component-inventory.md`](../docs/design-system/component-inventory.md)
- Machine-readable evidence: [`../docs/design-system/evidence/`](../docs/design-system/evidence/)

These tokens are an evidence-based internal baseline, not an official Asia Allied brand manual. Public CSS, fonts, logos, images, copy and the `wico` icon font are not vendored here. Evidence contains factual counts and bounded selector/value excerpts for traceability, not a reusable source stylesheet. Verify corporate approval and font/brand licensing before external production use.
