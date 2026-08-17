---
version: alpha
name: Asia Allied Corporate Digital
description: Evidence-based, accessibility-corrected digital design system derived from the public Asia Allied Infrastructure website for company admin, CMS and operational products.
colors:
  primary: "#006A63"
  primary-dark: "#003531"
  primary-active: "#001C19"
  accent: "#E6762D"
  accent-accessible: "#B15315"
  accent-selected: "#733208"
  text: "#333333"
  text-muted: "#6C757D"
  surface: "#FFFFFF"
  surface-subtle: "#F7F7F7"
  surface-muted: "#ECECEC"
  surface-disabled: "#EAEAEA"
  border: "#CECECE"
  table-header: "#FFF2EA"
  focus: "#006A63"
  danger: "#DC3545"
  success: "#006A63"
  logo-orange: "#F7941D"
  logo-olive: "#7B7A1B"
typography:
  display-lg:
    fontFamily: Pragati Narrow
    fontSize: 3.125rem
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0em"
  heading-xl:
    fontFamily: Pragati Narrow
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0em"
  heading-lg:
    fontFamily: Pragati Narrow
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0em"
  heading-md:
    fontFamily: Roboto
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0em"
  heading-sm:
    fontFamily: Roboto
    fontSize: 1.25rem
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0em"
  body-lg:
    fontFamily: Roboto
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  body-md:
    fontFamily: Roboto
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  body-sm:
    fontFamily: Roboto
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "0em"
  label:
    fontFamily: Roboto
    fontSize: 0.875rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0.01em"
  caption:
    fontFamily: Roboto
    fontSize: 0.75rem
    fontWeight: 400
    lineHeight: 1.35
    letterSpacing: "0.01em"
rounded:
  none: 0px
  sm: 2px
  md: 4px
  pill: 999px
spacing:
  2xs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 40px
  3xl: 48px
  4xl: 64px
  5xl: 80px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  button-accent:
    backgroundColor: "{colors.accent-accessible}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  navigation-active:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: 12px
  input-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  input-disabled:
    backgroundColor: "{colors.surface-disabled}"
    textColor: "{colors.text}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px
    height: 44px
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  page-canvas:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.text}"
  panel-muted:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.text}"
    rounded: "{rounded.none}"
    padding: 16px
  table-header:
    backgroundColor: "{colors.table-header}"
    textColor: "{colors.text}"
    typography: "{typography.label}"
    padding: 12px
  metadata:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-muted}"
    typography: "{typography.body-sm}"
  status-success:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.success}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-danger:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.danger}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-warning:
    backgroundColor: "{colors.accent-selected}"
    textColor: "{colors.surface}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: 8px
  section-accent-rule:
    backgroundColor: "{colors.accent}"
    height: 2px
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  focus-indicator:
    backgroundColor: "{colors.focus}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
  logo-orange-swatch:
    backgroundColor: "{colors.logo-orange}"
    size: 24px
  logo-olive-swatch:
    backgroundColor: "{colors.logo-olive}"
    size: 24px
---

# Asia Allied Corporate Digital Design System

## Overview

This is an evidence-based digital baseline derived from the public Asia Allied Infrastructure Holdings website, not an official corporate brand manual. The 2026-08-14 audit exhaustively parsed all three published sitemaps and inspected a deterministic cross-section of page templates, the live DOM, computed desktop/mobile styles, the public CSS and current logo assets.

The source character is practical, established and engineering-led: dark green provides structure and trust; orange supplies restrained momentum and emphasis; layouts are square, image-led and information-dense; typography is narrow and authoritative for English display copy and neutral for operational content.

For internal admin, CMS and operational products, preserve the identity rather than copying the public site's page composition. Use a predictable application shell, accessible controls, explicit states and reusable primitives. The public hero carousel, mega-menu and content-heavy footer are source patterns, not mandatory product components.

## Colors

### Normative production palette

| Token | Value | Production role |
|---|---:|---|
| `primary` | `#006A63` | Primary actions, links, selection and active navigation |
| `primary-dark` | `#003531` | Hover, pressed framing and high-density navigation |
| `primary-active` | `#001C19` | Active/pressed state where stronger separation is required |
| `accent` | `#E6762D` | Decorative rules, large headings, charts and non-text emphasis |
| `accent-accessible` | `#B15315` | Normal-sized white-on-orange interactive surfaces |
| `accent-selected` | `#733208` | Selected warning/tag surfaces with white text |
| `text` | `#333333` | Primary body and interface text |
| `text-muted` | `#6C757D` | Secondary metadata on white only |
| `surface` | `#FFFFFF` | Main surface, cards and reversed text |
| `surface-subtle` | `#F7F7F7` | Alternate rows and page canvas |
| `surface-muted` | `#ECECEC` | Muted structural regions |
| `surface-disabled` | `#EAEAEA` | Disabled controls |
| `border` | `#CECECE` | Dividers and control boundaries |
| `table-header` | `#FFF2EA` | Warm table/list header tint |
| `danger` | `#DC3545` | Error/destructive text and borders |
| `success` | `#006A63` | Positive states, always paired with a label/icon |

### Source evidence and classification

The current `projectbase.css` contains 2,883 parsed rules. Site-specific recurring values include `#E6762D` (60 declarations), `#006A63` (32), `#F7F7F7` (14), `#AAAAAA` (11), `#003531` (10), `#333333` (9), `#ECECEC` (8), `#CECECE` (7), `#733208` (4), `#B15315` (4), `#FFF2EA` (3) and `#EAEAEA` (3). Complete declaration counts/property distributions and a bounded set of selector/value examples—including bundled Bootstrap colors that are not promoted to brand tokens—are stored in `docs/design-system/evidence/css-token-evidence.json`.

Observed values and normative roles are intentionally separate: the public CSS uses `#B15315` in hover shadow/framing declarations, not as its standard orange button fill. Promoting it to `accent-accessible` is an accessibility-led product decision based on its 5.10:1 white-text contrast. Likewise, the spacing scale, 44px controls and normalized typography in this document are production rules, not claims of literal source extraction.

Observed state values retained as evidence but not promoted to independent normative tokens include:

- orange button hover `#DF681B`;
- deep-green button hover `#001C19`;
- form success `#28A745` and danger `#DC3545` from the bundled Bootstrap layer;
- generic Bootstrap blue focus `#007BFF` / `rgba(0, 123, 255, 0.25)`, which production implementations must replace with the green focus token;
- placeholder/card-image grey `#AAAAAA`, which is an implementation fallback rather than a product surface;
- pagination text `#707070` and light dividers `#EBEBEB`.

The current main logo PNG was independently sampled: dominant opaque pixels are dark `#231F20`, orange `#F7941D` and olive `#7B7A1B`. Keep `logo-orange` and `logo-olive` inside approved brand marks; do not repurpose them for product statuses or controls. The tagline image uses closely rendered/rasterized `#F49233` and `#7C7835`, which must not replace the canonical main-logo values.

### Contrast contract

- White on `primary` is **6.48:1**.
- White on `primary-dark` is **13.52:1**.
- White on `accent` is only **3.00:1**; never use this pairing for normal text.
- White on `accent-accessible` is **5.10:1**.
- White on `accent-selected` is **9.59:1**.
- `text` on white is **12.63:1**.
- `text-muted` on white is **4.69:1** and must not be placed on darker grey surfaces.
- `danger` on white is **4.53:1**, narrowly passing AA for normal text; prefer larger/bold error labels and never rely on red alone.
- `border` is not a text color and does not need text contrast, but interactive boundaries need sufficient non-text contrast or an additional focus indicator.

Never use color as the sole status cue. Add text and, where useful, an accessible icon.

## Typography

### Observed source typography

The current site self-hosts:

- Pragati Narrow 400 and 700;
- Roboto 300, 400, 500 and 700;
- a custom `wico` icon font.

The body stack is `Roboto, Arial, Microsoft JhengHei, Helvetica, sans-serif` with a source root size of `100.1%` and base line height `1.3`. English display headings, navigation, buttons, cards and labels use Pragati Narrow first. Traditional/Simplified Chinese year headings explicitly switch to Microsoft JhengHei.

Computed cross-checks on the current About page:

| Element | Desktop 1440px | Mobile 375px |
|---|---|---|
| Root/body | `16.016px`; body line height `20.821px` | Same |
| Page H1 | Pragati Narrow 700, `50.05px/50.05px`, green | `25.025px/25.025px`, green |
| Content H2 | Roboto 700, `24.024px/30.03px` | `17.017px/21.271px` |
| Content paragraph | Roboto 400, `18.018px/28.028px` | `14.014px/21.8px` |
| Breadcrumb | Roboto 400, `14.014px`, green | `12.012px`, hidden on sampled page |

### Production rules

- Use Roboto for product UI, forms, tables, body copy and numerical data.
- Use Pragati Narrow selectively for English display headings, section titles and compact corporate emphasis.
- For Chinese UI, use a verified CJK sans stack such as `Noto Sans TC`, then `Microsoft JhengHei`; do not force Pragati Narrow onto Chinese glyphs.
- Use weight 400 or above for operational copy. Source weight 300 is documentary evidence, not a default.
- Keep essential labels at 14px or larger and body copy at 16px where space allows.
- Use the normative product line heights in front matter rather than copying the source body's tight `1.3` everywhere.
- Do not use the source `wico` font in new products. Use the approved SVG icon library with accessible names and pinned licensing.
- If fonts are bundled, preserve their upstream licences. The current Google Fonts distributions of [Roboto](https://github.com/google/fonts/blob/main/ofl/roboto/OFL.txt) and [Pragati Narrow](https://github.com/google/fonts/blob/main/ofl/pragatinarrow/OFL.txt) are OFL-1.1; do not assume the public site's hosted files grant redistribution rights.

## Layout

### Source grid and responsive evidence

The source CSS uses Bootstrap-era breakpoints plus a wide corporate extension:

| Name | Min width | Source container max |
|---|---:|---:|
| compact | `370px` | fluid |
| sm | `576px` | `540px` |
| md | `768px` | `720px` |
| lg | `992px` | `960px` |
| xl | `1200px` | `1140px` |
| xxl | `1600px` | `1570px` |

The stylesheet contains corresponding max-width queries at `575.98`, `767.98`, `991.98`, `1199.98` and `1599.98px`. The public content uses three/two/one-column card changes and turns data tables into labelled stacked rows on narrow viewports.

### Production spacing

Use a 4px base with the named 4/8/12/16/24/32/40/48/64/80px scale. Source CSS uses many `em` fractions because components scale from local font size; production code must map those relationships to named tokens instead of copying long decimal values.

- 4–8px: icon and compact metadata gaps.
- 12–16px: control internals and related field spacing.
- 24px: normal card padding and component groups.
- 32–48px: page regions and major form sections.
- 64–80px: major marketing/content separation only.

### Admin and CMS composition

- Use a stable application shell rather than the public hero/mega-menu composition.
- Keep the page title, primary action and essential status visible without scrolling.
- Use readable form widths while allowing tables/dashboards to use available workspace.
- Keep filters adjacent to the data they affect.
- Use 44px minimum interactive height; use 48–56px rows normally and 40–44px only for an explicit compact mode.
- Stack forms/cards on narrow screens. Convert tables to labelled rows or horizontal scroll according to information priority; never silently hide critical columns.
- Preserve English and Traditional Chinese hierarchy when labels expand.

## Elevation & Depth

The source relies on color blocks, photography, alignment and borders more than floating elevation. The CSS contains many legacy shadows, but they are interaction effects rather than a multi-level elevation system.

- Default cards use a 1px border before a shadow.
- Use one restrained low elevation only when border/surface separation is insufficient.
- A suitable low elevation adaptation is `0 4px 12px rgba(0, 0, 0, 0.10)`; it is a production normalization, not a literal source token.
- Source interaction examples include card hover shadows around `rgba(0,0,0,0.10–0.20)`, a search overlay shadow at `rgba(0,0,0,0.30)` and mobile navigation at `rgba(0,0,0,0.20)`.
- Do not use glassmorphism, glow or heavy layered shadows.
- Focus indication must include a visible outline/ring and must not depend on shadow alone.

Motion evidence: the source's shared transition is `600ms cubic-bezier(0.23, 1, 0.32, 1)`, with 300ms links, 400ms image plates and 900ms banner text. Product controls should normally use 150–200ms feedback and reserve slower brand motion for non-blocking content. Respect `prefers-reduced-motion` and remove non-essential movement.

## Shapes

The source is predominantly square. Custom buttons and form overrides use `0px`; generic bundled Bootstrap controls use 3.2–4.8px radii; circles appear for dots/icons; one video affordance uses an approximately 4px local radius.

- `none`: navigation rails, structural panels and data-heavy regions.
- `sm`: compact embedded elements.
- `md`: fields, buttons, cards and dialogs.
- `pill`: status badges only.
- Do not introduce 12–24px consumer-style rounding or mix multiple corner languages on one screen.

## Components

The full observed inventory, variants, page-template coverage and production disposition are in `docs/design-system/component-inventory.md`. The public site exposes these families:

1. global header, utility links, language switcher, site search, desktop mega-navigation and mobile menu;
2. breadcrumb, page title, page-level navigation and back-to-top;
3. key visual/hero carousel with dots and pause/play control;
4. image-title, image-card, image-overlay, overlay-cover, left-image, top-image and image-plate card families;
5. section/related headings, rich text, side information, metadata, tags and social sharing;
6. tag filters, custom selects, pagination/load-more and responsive listing tables;
7. form controls, checkbox/radio, validation, reCAPTCHA dropdown and subscription/contact forms;
8. year accordion, development-history timeline and corporate-structure tree;
9. global-footprint map with selectable locations;
10. report/download, news, press release, e-news, career, people/director and project detail patterns;
11. footer link groups, social links, contact information and copyright.

### State contract for new components

Every interactive component must define default, hover, focus-visible, active/pressed, disabled and pending states where applicable. Data surfaces also need loading, empty, error, success and unauthorized states. Destructive actions require a consequence-aware confirmation.

### Buttons

- Primary: green surface/white label; dark green hover; near-black green active.
- Secondary: white surface, green text and visible green border.
- Accent: use `accent-accessible`, never raw `accent`, behind normal white text.
- Destructive: semantic red, visually separated from the primary action.
- Use sentence-case, action-specific labels.

### Forms

- Keep labels visible; placeholders are examples, not labels.
- Source controls are square, pale `#F7F7F7`, borderless and approximately 35.6px high; production controls deliberately increase to 44px and restore a visible boundary.
- Replace the source Bootstrap blue focus ring with the green focus token.
- State required/optional/help/error information in text and connect it with accessible descriptions.

### Tables and lists

- Source tables use white/`#F7F7F7` alternating rows and `#FFF2EA` headers; orange hover is documentary evidence but must not be the only row-action cue.
- Preserve column meaning on mobile with labelled stacked rows or controlled horizontal scrolling.
- Keep selection, sorting, filtering, pagination, loading, empty and error behavior explicit.

### Cards and media

- Use cards for meaningful grouping, not decoration around every section.
- Photography must communicate a real project, person or asset. Use responsive images with explicit dimensions and alternative text.
- Image overlays must prove text contrast in every image state; do not rely on an uncontrolled photograph.
- Do not copy the source's placeholder grey as a final asset.

### Navigation and feedback

- Current location must be explicit through position, label and color.
- Keep keyboard order logical and focus visible.
- Status badges combine label, shape and color.
- Toasts do not replace inline form errors.
- Preserve request/support IDs in recoverable operational errors.

## Do's and Don'ts

### Do

- Use deep green as the structural anchor and orange as a restrained accent.
- Build from the normative tokens and component contracts rather than hardcoded page colors.
- Use real infrastructure/project imagery when it improves understanding.
- Keep operational products clear, moderately dense and predictable.
- Validate every text/background pairing to WCAG AA and test focus/non-text contrast.
- Support English and Traditional Chinese without changing information hierarchy.
- Preserve loading, empty, error, success, unauthorized, pending and destructive states.
- Re-run the evidence audit when the source stylesheet hash changes.

### Don't

- Do not claim this extraction is the official corporate brand manual.
- Do not copy the public homepage, carousel or mega-menu into an admin shell.
- Do not place normal-sized white text on `#E6762D`.
- Do not use logo orange/olive as generic product status colors.
- Do not introduce pink, neon, glassmorphism or unrelated gradients.
- Do not use giant rounded cards or consumer-app softness.
- Do not use project photography behind essential text without a tested overlay.
- Do not import the public site's CSS, logo files, icon font or content into this repository; the audit records factual tokens and patterns only.

## Source and verification

- Public site: <https://www.asiaalliedgroup.com/en>
- Robots policy: <https://www.asiaalliedgroup.com/robots.txt>
- English sitemap: <https://www.asiaalliedgroup.com/sitemap.xml>
- Traditional Chinese sitemap: <https://www.asiaalliedgroup.com/sitemap-tc.xml>
- Simplified Chinese sitemap: <https://www.asiaalliedgroup.com/sitemap-sc.xml>
- Public stylesheets: `assets/css/projectbase.css`, `assets/css/print.css`
- Current project stylesheet SHA-256: `ff62bae815e73cb956e935b15bb4df7bec36e6c8013c38bd69a8bc7ab3f5dc94`
- Current print stylesheet SHA-256: `b99d6336f7da208f0d859a30cdbd0fb3e2cb1cff138732013a208751d9ae2e98`
- Current main logo SHA-256: `3d416329cccb7610860b26eb8d39d7dc9d5eab34677a654f81e51840c67a3566`
- Audit date: 2026-08-14
- Reproducible audit: `python3 scripts/audit_aai_design_system.py --audit-date YYYY-MM-DD`
- Evidence: `docs/design-system/evidence/`

The three sitemaps contained 10,669 entries (10,666 unique) at audit time. The audit parsed all entries, classified every route signature and fetched 100 deterministic representative pages spanning every locale/category/depth combination plus explicit high-value templates. All 100 returned without audit errors; across the sample set, only the two expected local stylesheets were discovered. This is exhaustive sitemap analysis with template-based page fetching; it is not a claim that every content URL was individually downloaded.
