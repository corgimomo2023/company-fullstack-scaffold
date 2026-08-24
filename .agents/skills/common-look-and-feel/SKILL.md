---
name: common-look-and-feel
description: Use when applying the company UI visual baseline.
version: 1.1.0
author: Platform Engineering
license: Internal
metadata:
  hermes:
    tags: [design-system, frontend, accessibility, admin, asia-allied]
    related_skills: []
---

# Common Look and Feel

## Overview

Apply the evidence-based, accessibility-corrected company visual baseline without copying the public website or forcing one product layout onto every application. This skill is a delivery procedure; root `DESIGN.md` is the normative token and component contract.

The baseline was derived from public Asia Allied Infrastructure website evidence. It is **not an official corporate brand manual**. Obtain brand-owner approval before external publication or trademark-sensitive use.

## When to use

Use this skill when:

- creating or restyling a company frontend screen;
- reviewing color, typography, spacing or component consistency;
- building an admin, CMS or operational interface;
- translating an approved mockup into React/Vite/Tailwind components.

Do not use it to clone the public website, infer confidential brand rules, replace product requirements, or make every application look like an admin dashboard.

## Source precedence

Read these sources in order before changing UI:

1. Root `AGENTS.md` and the nearest module `AGENTS.md` define engineering constraints.
2. Product requirements and existing feature boundaries define behavior and information architecture.
3. Root `DESIGN.md` defines normative visual tokens, component contracts, responsive behavior and accessibility rules.
4. `design-system/` contains generated implementation artifacts. Never hand-edit them.
5. `docs/design-system/source-evidence.md` is the clickable token/component evidence register. Use it whenever changing or challenging a token, visual variant or public-pattern mapping.
6. `references/asia-allied-baseline.md` explains provenance, evidence classes and usage limits.
7. `templates/admin-cms.html` is a static composition reference for admin/CMS screens only.

If root `DESIGN.md` or required generated artifacts are absent, stop and report the missing prerequisite. Do not reconstruct values from memory or scrape the live website during normal feature work.

## Choose the product profile

Choose a profile before choosing layout:

- **Admin / CMS / operations:** use `templates/admin-cms.html` as a composition reference. Preserve the product's actual navigation and data model.
- **Public corporate website:** use the shared tokens but create a content-led public layout with approved imagery. Do not reuse the admin sidebar or dense data table composition.
- **Field / site safety:** prioritize touch targets, daylight contrast, short forms, offline/error recovery and task status. Do not reuse the admin density by default.
- **Campaign:** use the shared brand palette but establish campaign-specific art direction and approved media.
- **Project showcase:** prioritize photography, project metadata and narrative hierarchy rather than dashboard statistics.

Only the Admin / CMS profile has a bundled HTML reference in version 1.0. Other profiles require a separately reviewed mockup; never imply a missing template exists.

## Procedure

1. **Define the screen contract.** Record actor, top task, data density, language, viewport range, loading/empty/error/unauthorized states and destructive actions.
2. **Inspect the existing frontend.** Preserve routing, component boundaries, state management, translations and API contracts. Do not replace the application shell unless the task requires it.
3. **Load the normative contract.** Read root `DESIGN.md`; use generated `design-system/foundation.css`, `design-system/theme.css`, `design-system/tailwind.preset.cjs`, `design-system/tailwind.theme.json`, `design-system/tokens.json` or `design-system/components.json` for the target stack. Never hand-edit generated artifacts.
4. **Use the correct reference.** For Admin / CMS, open `templates/admin-cms.html`. Reuse its hierarchy and visual rhythm, not its sample words, counts or domain model.
5. **Map semantics, not raw hex values.** Use semantic names such as `primary`, `accent-accessible`, `text-muted`, `table-header` and `focus`. Brand orange is decorative; use the accessible orange token for normal-size white text. Check `components.json` implementation coverage: `behavior-only` means behavior is required but a finished visual mapping must not be assumed.
6. **Compose reusable production components.** In React/Vite, split the shell, navigation, filters, cards, tables, forms, feedback and dialogs. Do not place the whole screen in one component or copy static HTML verbatim.
7. **Complete interaction states.** Implement loading, empty, error, unauthorized, pending, disabled and success states. Destructive actions require a consequence-bearing confirmation. Recoverable errors expose the request/support ID when available.
8. **Apply language and media rules.** Support English and Traditional Chinese content expansion. Use approved, meaningful images with useful alt text for public/showcase work; decorative imagery uses empty alt text. Never hotlink public-site assets.
9. **Verify real rendering.** Exercise keyboard order and focus, then inspect at approximately 1440px, 768px and 390px. Check overflow, table behavior, navigation, 44px touch targets and zoom/reflow.
10. **Cross-check evidence when changing the baseline.** Use the exact CSS declaration/media-query or live URL + DOM location listed in `docs/design-system/source-evidence.md`. Compare a viewport/state only when the record links to a specific computed result; otherwise preserve `not observed`. Preserve raw-value, normalized-semantic and accessibility-correction classifications.
11. **Run repository gates.** Run the narrow behavior test, generated-artifact drift check, evidence-register drift check and then `make check`. Record only checks that actually passed.

## Visual rules

- Use teal for structure, navigation and high-emphasis actions.
- Use orange sparingly for emphasis. Do not use the observed brand orange behind normal-size white text when contrast fails.
- Keep light surfaces, restrained borders and modest shadows. Avoid generic dark SaaS shells, giant radii, glassmorphism and decorative gradients that replace information hierarchy.
- Use Pragati Narrow for approved display roles and Roboto for product UI roles, with the CJK fallback stack defined in `DESIGN.md`.
- Prefer Lucide for new React/Vite interfaces. Use Bootstrap Icons in Bootstrap-standardized products or Font Awesome Free only when catalogue/brand coverage is required. Do not standardize on `react-icons`.
- Do not copy selectors, compiled CSS, fonts, logo binaries or content from the audited public website.

## Accessibility contract

- WCAG 2.2 AA is the minimum target.
- All interactive controls need visible `:focus-visible` treatment.
- Controls and primary touch targets should be at least 44px high where practical.
- Do not communicate status by color alone.
- Tables need semantic headers, a responsive strategy and an accessible name where context is not obvious.
- Forms need persistent labels, useful error text and programmatic error association.
- Dialogs need focus management, Escape behavior and focus return in production code.
- Respect reduced-motion preferences and preserve content at 200% zoom.

## Verification checklist

- [ ] Correct profile selected; no admin layout copied into another profile
- [ ] Root `DESIGN.md` read and generated artifacts left untouched
- [ ] Changed token/component cross-checked against its clickable source evidence
- [ ] `behavior-only` states were not described as visually implemented
- [ ] Existing architecture, routes and translations preserved
- [ ] No raw public-site CSS/assets or unapproved trademark use
- [ ] Loading, empty, error, unauthorized, pending and destructive states covered
- [ ] Keyboard, focus, responsive and Traditional Chinese content checked
- [ ] No hardcoded credentials, private hosts, internal URLs or personal paths
- [ ] Narrow tests and `make check` passed

## Pitfalls

- The public-site audit is evidence, not a pixel-perfect cloning instruction.
- The accessibility-corrected orange is a product-system decision, not a claim about the live website.
- `templates/admin-cms.html` is intentionally static and dependency-free; add real behavior through the project's established components.
- Do not add CDN scripts, remote fonts or hotlinked images to the bundled template.
- Never claim that all public URLs were fetched or that an existing frontend has already been migrated.
- Do not equate sitemap inventory, normalized route HTTP coverage and responsive rendered-profile coverage; report each separately.
