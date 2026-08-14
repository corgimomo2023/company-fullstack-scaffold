---
version: alpha
name: Asia Allied Corporate Digital
description: An evidence-based digital design baseline derived from the public Asia Allied Infrastructure website for company internal applications and admin surfaces.
colors:
  primary: "#006A63"
  primary-dark: "#003531"
  accent: "#E6762D"
  accent-accessible: "#B15315"
  text: "#333333"
  text-muted: "#6A6A6A"
  surface: "#FFFFFF"
  surface-subtle: "#F7F7F7"
  surface-muted: "#ECECEC"
  border: "#CECECE"
  focus: "#006A63"
  danger: "#B42318"
  danger-surface: "#FEE4E2"
  success: "#006A63"
  success-surface: "#E5F3F1"
typography:
  display-lg:
    fontFamily: "Pragati Narrow, Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  heading-xl:
    fontFamily: "Pragati Narrow, Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.005em"
  heading-lg:
    fontFamily: "Pragati Narrow, Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0em"
  heading-md:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 1.25rem
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0em"
  body-lg:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "0em"
  body-md:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "0em"
  body-sm:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.45
    letterSpacing: "0em"
  label:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
    fontSize: 0.875rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0.01em"
  caption:
    fontFamily: "Roboto, Arial, Microsoft JhengHei, sans-serif"
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
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
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
  card-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 24px
  status-success:
    backgroundColor: "{colors.success-surface}"
    textColor: "{colors.success}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: 8px
  status-danger:
    backgroundColor: "{colors.danger-surface}"
    textColor: "{colors.danger}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: 8px
  section-accent-rule:
    backgroundColor: "{colors.accent}"
    height: 2px
  page-canvas:
    backgroundColor: "{colors.surface-subtle}"
    textColor: "{colors.text}"
  table-header:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.text}"
    typography: "{typography.label}"
    padding: 12px
  metadata:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-muted}"
    typography: "{typography.body-sm}"
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  focus-indicator:
    backgroundColor: "{colors.focus}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
---

# Asia Allied Corporate Digital Design System

## Overview

This file is an evidence-based digital baseline derived on 2026-08-13 from the public website at <https://www.asiaalliedgroup.com/>. It is intended to give coding agents and product teams a consistent company look and feel for internal applications, especially admin, CMS and operational interfaces.

It is not represented as an official corporate brand manual. The source website was inspected through its rendered interface, computed browser styles, public stylesheet and public logo assets. Production tokens preserve the observed visual character while correcting accessibility risks found in literal reuse.

The design character is:

- established Hong Kong infrastructure and engineering group;
- practical, stable and corporate rather than playful;
- image-led where project photography adds context;
- high-contrast dark green structural surfaces;
- restrained orange emphasis for momentum, headings and highlights;
- square, engineered geometry with minimal decoration;
- information-dense but orderly for operational use.

For admin and CMS products, use the colors, typography, spacing and interaction semantics in this file. Do not copy the public website's page composition, hero carousel or content-heavy footer into internal products.

## Colors

### Observed source palette

The public website's recurring UI colors are:

| Role observed | Value | Evidence |
|---|---|---|
| Structural green | `#006A63` | Navigation, announcement and report surfaces; 32 stylesheet occurrences |
| Deep green | `#003531` | Dark overlays and navigation states |
| Orange accent | `#E6762D` | Headings, section rules, labels and subscription surface; 60 stylesheet occurrences |
| Logo orange | `#F7941D` | Dominant orange sampled from public logo asset |
| Logo olive | `#7B7A1B` | Secondary logo color sampled from public logo asset |
| Primary text | `#333333` | Dominant computed text color |
| Muted text | `#6A6A6A` | Secondary computed text color |
| Border | `#CECECE` | Light dividers and borders |
| Pale surface | `#F7F7F7` | Section and card surfaces |
| White | `#FFFFFF` | Main canvas, cards and reversed text |

### Accessible production use

- Use `primary` (`#006A63`) for primary actions, active navigation, selected controls and high-emphasis operational states. White on this green has a measured contrast ratio of approximately **6.48:1**.
- Use `primary-dark` (`#003531`) for hover, pressed, high-density navigation and dark overlays. White on this green is approximately **13.52:1**.
- Use `accent` (`#E6762D`) for decorative rules, large headings, charts and non-text emphasis. White on this orange is only approximately **3.00:1**, so it must not be used for normal-sized white button text.
- Use `accent-accessible` (`#B15315`) when orange carries normal-sized text or an interactive foreground. White on this darker orange is approximately **5.10:1**.
- Use `text` (`#333333`) for body copy on white or pale surfaces. It provides approximately **12.63:1** against white.
- Use `text-muted` (`#6A6A6A`) only for secondary text. It provides approximately **5.41:1** against white.
- Keep logo colors reserved for approved logos and brand marks. Do not recolor text, controls or status states merely to mirror the logo.
- Never use color as the only indicator of status. Pair it with text and, where useful, a recognizable icon.

### Semantic hierarchy

- **Primary green:** action, trust, navigation, governance and completion.
- **Deep green:** authority, hierarchy, hover and structural framing.
- **Orange:** momentum, highlight, attention and corporate energy.
- **Neutral greys:** working surfaces, dividers, metadata and supporting hierarchy.
- **Red:** destructive or failure states only; never substitute orange for danger.

## Typography

The public website loads Roboto weights 300, 400, 500 and 700; Pragati Narrow weights 400 and 700; and falls back to Arial, Microsoft JhengHei and Helvetica. Rendered body content primarily uses Roboto, while navigation and prominent labels frequently use Pragati Narrow.

Apply the system as follows:

- Use **Roboto** for product UI, forms, tables, long-form copy and numerical information.
- Use **Pragati Narrow** selectively for English display headings, navigation labels and compact corporate emphasis.
- Use **Microsoft JhengHei** as the preferred Traditional Chinese fallback.
- Do not use light weight 300 for small operational copy; prefer 400 or above.
- Keep body text at 16px where space allows. Never reduce essential labels below 14px.
- Use weight and spacing for hierarchy before introducing more colors.
- Preserve comfortable line height for bilingual English and Chinese content.

## Layout

### Foundation

Use a 4px base unit with an 8px practical spacing rhythm. Prefer the named spacing tokens over arbitrary values.

- `xs` and `sm`: icon gaps, compact metadata and tightly related controls.
- `md`: default form and component spacing.
- `lg`: card padding and section grouping.
- `xl`: page-level spacing.
- `2xl` and `3xl`: major section separation on wide screens.

### Admin and CMS composition

- Use a stable application shell rather than the public website's hero/navigation composition.
- Keep page titles, primary action and essential status visible without scrolling.
- Use a maximum readable width for forms, but allow tables and dashboards to use the available workspace.
- Keep filters close to the data they affect.
- Align labels, values and actions consistently across list and detail views.
- Collapse secondary actions into an overflow menu before reducing label clarity.
- On narrow screens, stack forms and cards; do not compress desktop tables until content becomes unreadable.

### Density

The visual tone is structured and information-forward. Use moderate density by default:

- 44px minimum interactive height;
- 48–56px table rows for normal mode;
- 40–44px rows only for an explicit compact admin mode;
- 16–24px card padding;
- visible separation between page regions rather than decorative cards around every item.

## Elevation & Depth

The public identity relies more on color blocks, photography and alignment than on floating elevation. Keep shadows restrained.

- Default cards use a border before a shadow.
- Use one low elevation level only where separation from the canvas is otherwise unclear.
- Do not apply glow, glassmorphism or heavy layered shadows.
- Dark-green overlays may be used on imagery only when contrast is verified.
- Focus indication must not depend on box shadow alone; retain a visible outline or ring.

## Shapes

The source website is predominantly square (`0px` radius), with small Bootstrap-era radii on generic controls. For modern internal products, preserve the engineered tone using a restrained radius scale:

- `none`: navigation rails, structural panels and data-heavy regions.
- `sm`: compact indicators or embedded elements.
- `md`: buttons, fields, cards and dialogs.
- `pill`: status badges only.

Avoid oversized 12–24px consumer-style rounding. Avoid mixing multiple corner styles in one screen.

## Components

### Application shell

- White or pale working canvas.
- Deep-green navigation or a white navigation surface with deep-green active state.
- Orange appears as a small accent, not as the full application chrome.
- Product identity, environment and signed-in actor remain visible.

### Buttons

- Primary action: green surface, white text.
- Secondary action: white surface, green text and visible green border in implementation.
- Accent action: dark accessible orange only when a second high-emphasis action is genuinely required.
- Destructive action: semantic red, separated from the primary action.
- Every button must expose hover, focus, active, pending and disabled states.
- Use sentence-case action labels. Do not use vague labels such as “Submit” when “Create project” is clearer.

### Forms

- Labels remain visible above or beside inputs; placeholders are examples, not labels.
- Required, optional, error and help states are explicit in text.
- Inputs use white surfaces, dark text, restrained borders and a visible green focus treatment.
- Group related fields with spacing and headings rather than excessive boxes.
- Validation errors identify both the problem and corrective action.

### Tables and lists

- Use green sparingly for selected or actionable states.
- Use orange only for non-semantic emphasis; warning states require text and an accessible semantic treatment.
- Provide loading, empty, error and success states.
- Keep row actions consistent and keyboard accessible.
- Preserve identifiers and request IDs where operational support needs them.

### Cards

- Use cards for meaningful grouping, not as decoration around every section.
- Default to white on pale grey with a restrained border.
- Project or asset photography may be used when it communicates real context.
- Avoid generic AI-generated corporate imagery and decorative gradients.

### Status and feedback

- Status badges use shape, label and color together.
- Toasts do not replace inline error messages for failed forms.
- Confirm destructive actions and explain the consequence.
- Show progress for operations that are not immediate.

### Navigation

- Keep labels direct and stable.
- Show the current section clearly through position, text and color.
- Maintain keyboard order and visible focus.
- For internal products, prefer a predictable sidebar or top navigation over the source site's large dropdown menu.

## Do's and Don'ts

### Do

- Apply deep green as the structural anchor and orange as a restrained accent.
- Use real infrastructure, people or project imagery when imagery improves understanding.
- Keep internal applications practical, clear and moderately dense.
- Support English and Traditional Chinese without changing hierarchy.
- Validate every text/background pairing to WCAG AA.
- Derive implementation tokens from this file rather than hardcoding page-level colors.
- Preserve loading, empty, error, success, unauthorized and destructive states.

### Don't

- Do not copy the public homepage layout into admin or CMS applications.
- Do not use `#E6762D` behind normal-sized white text.
- Do not use logo olive as a general status or interaction color.
- Do not introduce pink, neon, glassmorphism or unrelated gradients.
- Do not use giant rounded cards or consumer-app softness.
- Do not use project photography as a background behind essential operational text unless an accessible overlay is proven.
- Do not claim this extracted baseline is the official corporate brand manual.
- Do not add new colors without documenting their semantic role and contrast behavior.

## Source and review

- Public source inspected: <https://www.asiaalliedgroup.com/>
- Public stylesheet inspected: `assets/css/projectbase.css`
- Public assets sampled: `main-logo-1x.png`, `sub-logo-1x.png`
- Extraction date: 2026-08-13
- Review this baseline against any internal official brand guideline before treating it as corporate policy.
