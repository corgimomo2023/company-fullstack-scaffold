# Design-system artifacts

[`../DESIGN.md`](../DESIGN.md) is the normative source. The files in this directory are generated; do not edit them by hand.

| Artifact | Consumer | Contract coverage |
|---|---|---|
| [`theme.css`](theme.css) | Tailwind CSS v4 `@theme` import | Foundation tokens plus typography line-height variables |
| [`tailwind.theme.json`](tailwind.theme.json) | Tailwind CSS v3 `theme.extend` mapping | Foundation tokens plus composite font-size/line-height settings |
| [`tokens.json`](tokens.json) | DTCG Format Module 2025.10 consumers | Foundations and typography; components in a namespaced `$extensions` contract |
| [`components.json`](components.json) | Framework-neutral component tooling | All 21 component/variant contracts from `DESIGN.md` |

## Why a wrapper is required

`@google/design.md@0.4.0` is the pinned parser/exporter, but its raw exports omit typography `lineHeight` and produce DTCG `letterSpacing` values in an unsupported `em` unit. [`scripts/export_design_system.py`](../scripts/export_design_system.py) preserves line-height, converts relative letter-spacing to schema-valid `rem`, and carries the full component contract into both `components.json` and a namespaced DTCG extension.

## Regenerate and validate

```bash
pip install -r requirements-design.txt
npx -y @google/design.md@0.4.0 lint DESIGN.md
python3 scripts/export_design_system.py
python3 scripts/export_design_system.py --check

curl -fsSL https://www.designtokens.org/schemas/2025.10/format.json \
  -o /tmp/dtcg-format-schema.json
npx -y ajv-cli@5 validate --spec=draft7 --strict=false --all-errors \
  -s /tmp/dtcg-format-schema.json -d design-system/tokens.json
```

CI runs the same drift and official-schema checks.

## Tailwind v4

Import the generated theme after Tailwind:

```css
@import "tailwindcss";
@import "../../design-system/theme.css";
```

This exposes utilities such as `bg-primary`, `text-accent-accessible`, `rounded-md`, `p-lg` and `text-body-md`, plus `--leading-*` variables for every typography role. Font variables identify the preferred family only; load licensed font files separately and define fallback stacks in the application foundation layer.

## Tailwind v3

Merge `tailwind.theme.json` under the application's Tailwind configuration. Every named `fontSize` entry includes its normative line-height. Do not replace unrelated plugin/content settings.

## Framework-neutral use

`tokens.json` validates against the declared DTCG 2025.10 schema. Its colors use structured sRGB values plus a hex fallback. Component definitions are intentionally stored under the `com.github.corgimomo2023.company-fullstack-scaffold` extension because DTCG has no standard component-contract type; consumers that do not support extensions can read `components.json`.

If a downstream tool supports only legacy string colors, use the Tailwind JSON export or add a reviewed transform rather than weakening the canonical DTCG file.

## Evidence and ownership

- Research method and source integrity: [`../docs/design-system/source-audit.md`](../docs/design-system/source-audit.md)
- Components and page templates: [`../docs/design-system/component-inventory.md`](../docs/design-system/component-inventory.md)
- Machine-readable source evidence: [`../docs/design-system/evidence/`](../docs/design-system/evidence/)

These tokens are an evidence-based internal baseline, not an official Asia Allied brand manual. Public CSS, fonts, logos, images, copy and the `wico` icon font are not vendored here. Evidence contains factual counts and limited selector/value excerpts for traceability, not a reusable stylesheet. Verify corporate approval and font/brand licensing before external production use.
