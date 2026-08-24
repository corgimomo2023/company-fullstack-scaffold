---
name: common-look-and-feel-colors
description: Use when changing only a project's color palette.
version: 1.0.0
author: Platform Engineering
license: Internal
metadata:
  hermes:
    tags: [design-system, colors, palette, tailwind, refactor]
    related_skills: [common-look-and-feel]
---

# Common Look and Feel Colors

## Overview

Apply the company Common Look & Feel **colors only** to an existing project. This is a narrow palette refactor, not a redesign. Preserve the existing project's visual language, behavior, architecture and component composition; change only color tokens and color references.

The copyable files in this skill are deliberately color-only subsets of the generated design-system exports:

- `templates/tailwind.colors.json` for Tailwind configuration and other JSON-driven theme adapters;
- `templates/theme.colors.css` for Tailwind CSS v4 `@theme` color variables.

They are synchronized with `design-system/tailwind.theme.json` and `design-system/theme.css`, but exclude fonts, type scales, spacing, breakpoints, containers, radii, shadows and motion. Do not copy the full generated design-system files wholesale into an existing project.

## When to use

Use this skill when:

- an existing project must adopt the Common Look & Feel palette without redesigning its UI;
- a Tailwind v3/v4 project needs the approved semantic color names;
- hardcoded project colors need to be mapped to shared semantic colors;
- a color-only migration must preserve existing layouts and components.

Do not use this skill to create a new layout, normalize component geometry, replace a design system, change typography, or rebuild the application shell. Use the broader `common-look-and-feel` skill only when a full visual-system implementation was explicitly requested.

## Hard scope boundary

- Preserve the existing project layout, navigation, DOM hierarchy, component boundaries and responsive behavior.
- Do not change component structure or component behavior.
- Do not change typography, spacing, sizing, border radius, shadows, or motion.
- Do not redesign buttons, inputs, cards, dialogs, tables or navigation.
- Do not replace the application shell.
- Do not introduce new components merely to apply the palette.
- Do not rename unrelated classes, props, files, routes or translation keys.
- Do not apply formatting changes outside the exact color-related lines being edited.
- A component file may change only when replacing a hardcoded color or color utility with its mapped semantic token.

If a requested color cannot meet required contrast without changing geometry, typography or content, stop and report the conflict. Do not silently expand scope.

## Complete 18-token UI palette

The color-only skill exposes all **18 semantic UI tokens** from `DESIGN.md`. Logo artwork colors are intentionally excluded: consume the approved logo asset as an image and never recreate or repurpose sampled logo colors as product tokens.

The stakeholder reference deck is `docs/design-system/vibe-code-common-look-and-feel-colour-foundation.pptx`. It presents all 18 tokens with live website screenshot references and must remain logo-color-free. Treat `DESIGN.md` and the copyable templates as normative; the deck is a communication artifact and must not introduce additional tokens.

## Palette roles

Use semantic roles rather than selecting colors by visual similarity:

| Role | Intended use |
|---|---|
| `primary`, `primary-dark`, `primary-active` | Structural and high-emphasis brand actions |
| `accent` | Decorative emphasis and large text where contrast is sufficient |
| `accent-accessible` | Normal-size white-text actions requiring stronger contrast |
| `accent-selected` | Selected/active accent states |
| `text`, `text-muted`, `text-on-accent` | Existing text hierarchy, without changing type styles |
| `surface`, `surface-subtle`, `surface-muted`, `surface-disabled` | Existing surface hierarchy |
| `border` | Existing borders only; do not add borders |
| `table-header` | Existing table-header backgrounds |
| `focus` | Existing focus indication color; do not alter focus geometry |
| `danger`, `success` | Existing semantic states |

Never use color alone to communicate status. Preserve labels, icons and accessibility semantics already present in the project.

## Procedure

### 1. Freeze the non-color baseline

Before editing, record:

- a clean `git status` and the target revision;
- the current project build/test commands;
- screenshots of representative pages and interaction states;
- existing Tailwind/CSS theme entry points;
- computed non-color properties for representative components: font family, font size, line height, spacing, dimensions, border radius, shadow, layout mode and responsive behavior.

Completion criterion: the before-state can prove whether a later change affected anything other than color.

### 2. Copy the color-only inputs

When applying this skill, **copy both color-only files into the target project**. Keep their names or place them in a clearly named color-theme directory:

```bash
mkdir -p <target-project>/design-system/colors
cp <this-skill>/templates/tailwind.colors.json \
  <target-project>/design-system/colors/tailwind.colors.json
cp <this-skill>/templates/theme.colors.css \
  <target-project>/design-system/colors/theme.colors.css
```

Do not copy `design-system/tailwind.theme.json` or `design-system/theme.css` directly: those full exports include unrelated typography, spacing, radius, breakpoint, shadow and motion values.

Completion criterion: the target project contains `tailwind.colors.json` and `theme.colors.css`, and both contain palette declarations only.

### 3. Integrate with the project's existing Tailwind version

**Tailwind v3 / JavaScript configuration**

Read `tailwind.colors.json` and merge `theme.extend.colors` into the project's existing `theme.extend.colors`. Preserve every other existing Tailwind key. Do not replace `theme`, `extend`, `fontFamily`, `spacing`, `borderRadius`, `screens`, plugins, content paths or presets.

Conceptual merge:

```js
const palette = require('./design-system/colors/tailwind.colors.json')

// Copy every current theme.extend.colors entry here unchanged before adding
// the shared palette. This object represents the target project's baseline.
const existingProjectColors = {
  brandLegacy: '#123456',
  partnerSpecific: '#abcdef',
}

module.exports = {
  // preserve existing config
  theme: {
    // preserve existing theme keys
    extend: {
      // preserve existing extend keys
      colors: {
        ...existingProjectColors,
        ...palette.theme.extend.colors,
      },
    },
  },
}
```

The example's `existingProjectColors` is a placeholder: preserve every existing `theme.extend.colors` entry from the target config, not only the two sample entries. By default the shared palette wins only when the same semantic key conflicts, so the requested Common Look & Feel role is actually applied while unrelated project-specific colors remain available. Before replacing a conflicting semantic key, document its old value and all current usages. An explicitly approved project override may be applied after the shared palette, but must be recorded as a deliberate exception. Do not use a blind full-object overwrite.

**Tailwind CSS v4**

Import the copied color theme from the project's existing stylesheet after the Tailwind import:

```css
@import "tailwindcss";
@import "./design-system/colors/theme.colors.css";
```

The copied theme must contain only `--color-*` declarations. Do not import the repository's full `design-system/theme.css` into an existing project.

Completion criterion: the project exposes the approved semantic colors while all non-color Tailwind and CSS theme values remain byte-for-byte or semantically unchanged.

### 4. Refactor color references only

Inventory existing hardcoded hex/RGB/HSL values, CSS custom properties and Tailwind color utilities. Map each existing role to the closest approved semantic role before editing.

Allowed edits include:

- replacing `#174ea6` with `var(--color-primary)` in an existing declaration;
- changing `bg-blue-600` to `bg-primary` without changing any other utility;
- changing an existing border color to `border-border` without adding/removing the border;
- replacing an existing focus color while retaining its width, offset and style.

Not allowed:

- changing padding, gap, width, height or alignment;
- changing a button's radius, typography, icon, label or state behavior;
- changing component markup or extracting/recombining components;
- adding cards, wrappers, gradients, shadows, borders or decorative elements;
- replacing an existing layout or page template.

Completion criterion: every changed production line is directly attributable to a color token, color value or color utility.

### 5. Preserve state semantics and contrast

Check default, hover, active, selected, focus, disabled, error and success states that already exist. Use `accent-accessible` where normal-size light text over orange needs WCAG 2.2 AA contrast. Keep `accent` for decorative use or contexts where its actual foreground/size passes.

Do not fabricate a missing state. Do not change labels or interaction behavior to compensate for a palette choice.

Completion criterion: existing states remain distinguishable and required text/control contrast passes.

### 6. Verify color-only change

Run narrow tests and the project's complete quality gate. Compare before/after computed styles for the non-color properties captured in step 1. Review `git diff --word-diff` and `git diff --name-only`.

Fail the change if the diff alters any unrelated:

- component structure, layout or responsive rules;
- typography, spacing, dimensions or border radius;
- shadows, motion or interaction behavior;
- API, state, routing, data or translations.

Completion criterion: tests/build pass, rendered pages use the new palette, contrast checks pass, and the non-color baseline has no drift.

## Verification checklist

- [ ] Scope is colors only
- [ ] Existing project style and component structure are preserved
- [ ] Both color-only Tailwind files were copied into the project
- [ ] Tailwind v3 merged only `theme.extend.colors`, or Tailwind v4 imported only `--color-*` declarations
- [ ] No full generated theme file was copied wholesale
- [ ] Every production edit maps to a color value, token or utility
- [ ] Logo artwork colors are absent from the UI palette; approved logos are consumed as images
- [ ] Existing interaction states remain intact
- [ ] WCAG contrast was checked for changed foreground/background pairs
- [ ] Non-color computed styles match the before-state
- [ ] Narrow tests and full project gates pass
- [ ] No unrelated files or formatting changes are present

## Common pitfalls

1. **Replacing the full Tailwind theme.** This imports unrelated fonts, spacing, radii and breakpoints. Copy and merge only the supplied color-only files.
2. **Treating orange as a universal button fill.** Use the accessible semantic role when normal-size light text requires it.
3. **Sampling logo artwork into UI tokens.** Logo colors are excluded from this skill; consume the approved logo image instead.
4. **Changing geometry while “cleaning up” colors.** Revert all unrelated cleanup; this skill is intentionally narrow.
5. **Blind search-and-replace.** The same old hex may represent different semantic roles. Map usage by context.
6. **Reporting a redesign as a palette refactor.** If layout or component styling beyond color must change, stop and request separate scope.
