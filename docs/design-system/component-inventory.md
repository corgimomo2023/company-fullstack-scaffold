# Asia Allied component and page-pattern inventory

This inventory records components observed across the 2026-08-19 public-site audit and states how they should inform company products. Selectors are evidence labels, not code to copy. The public site's CSS, assets, content and custom icon font are not imported into this repository. Per-component live URLs, page locations, states and methods are in [`source-evidence.md`](source-evidence.md).

## Global component families

| Family | Source selectors / DOM evidence | Observed variants and states | Sample templates | Production disposition |
|---|---|---|---|---|
| Global header | `.page-head`, `.header__*`, `.menu` | Desktop white shell; compact/mobile `#ECECEC`; sticky/menu modes | All HTML templates | Rebuild as an app header; retain brand hierarchy, skip link and responsive behavior |
| Utility navigation | utility links, career/contact/language controls | EN/繁/簡 switching, stock ticker iframe | All HTML templates | Keep locale/account utilities concise; third-party ticker is not a scaffold primitive |
| Site search | `.sitesearch__wrap` | Hidden/open overlay, green surface, close/submit controls | All HTML templates | Implement an accessible dialog/combobox only where global search exists |
| Desktop navigation | `.mn__nav`, `.mn__list--1..4`, `.mn__link--2` | Multi-level hover/focus panels | Desktop shell | Internal products should use stable top/side navigation, not copy the mega-menu |
| Mobile menu | `.mb-mn__wrap`, `.mTrigger__open` | Closed/open, nested disclosure | Mobile shell | Use disclosure buttons with `aria-expanded`, focus containment and Escape |
| Breadcrumb | `.breadcrumb` | Green text, separators; hidden at the sampled mobile state | Interior pages | Keep only when hierarchy is deep; do not hide essential current-location context |
| Page title | `.page-title-wrap`, `.page-title` | 50px desktop / 25px mobile, green Pragati Narrow | Interior pages | Use normative heading tokens and one semantic H1 |
| Page menu | `.page-menu__link` | White-on-green local navigation | Group/IR sections | Use tabs/subnavigation only when sibling destinations are stable |
| Back to top | `.bk2Top__btn` | Hidden/shown by scroll, hover shadow | Widespread across HTML content routes | Optional for long content; provide accessible name and avoid icon-font glyphs |
| Footer | footer, `.ft-link-list`, `.soc-list` | Legal links, social links, contact/copyright; grey surface | All HTML templates | Keep legal/support essentials; internal apps should not reproduce the large public footer |

## Content and media families

| Family | Source selectors | Structure / behavior | Production contract |
|---|---|---|---|
| Hero/key visual | `.key-visual`, Slick classes | Image/video slides, dots, pause/play, shadowed indicators | Marketing/content only; pause control, keyboard support and reduced motion are mandatory |
| Image card | `.img-card-blk` | Large image-led card; orange Pragati Narrow title | Use for genuine projects/assets, not generic dashboard containers |
| Image-title card | `.img-title-blk` | Portrait image + green title + black description; green-to-orange hover | Preserve semantic heading/link; 3/2/1-column responsive layout |
| Image overlay card | `.img-overlay-blk` | Image with bottom text surface, type variants | Test text contrast independently from imagery |
| Overlay-cover card | `.overlay-cover-blk` | Green `rgba(0,106,99,.9)` overlay, white copy | Use only with deterministic overlay; ensure all text remains readable |
| Image plate | `.img-plate-blk` | Image plus plate/title/action; shadow on interaction | Use border-first elevation and explicit link affordance |
| Spaced image plate | `.img-space-plate-blk` | Image with detached content plate | Avoid layout-only duplication; map to a shared media-card primitive |
| Left image card | `.left-img-blk` | Fixed image area and text/action | Stack on narrow screens; preserve reading order in DOM |
| Top image card | `.top-img-blk` | Top media, body and action | Shared card primitive, not a separate visual system |
| Blog card/list | `.img-blog-blk`, `.img-blog-list` | Date/category/title/media and list variants | Use structured metadata and actual publication dates |
| Thumbnail list | `.thumb-blk`, `.thumb-blk-list` | Compact image/date/title rows | Ensure thumbnails have dimensions and meaningful alt text |
| Feature slider | `.feature-slider` | Image gradient + overlaid copy | Marketing only; avoid for core operational actions |
| Video link | `.video-link` | Thumbnail plus custom icon-font play marker | Replace with SVG icon and text label; disclose external destinations |
| Rich text | `.ckec`, `.cke_editable` | Headings, lists, tables, external-link markers and legacy CMS output | Sanitize content; provide stable prose/table styles; never expose editor-only classes as API |

## Data, discovery and control families

| Family | Source selectors | Observed behavior | Production contract |
|---|---|---|---|
| Tag filter | `.tag-list`, `.tag`, `.tag.selected` | Green variant; dark-orange selected/hover; compact variants | Use buttons, selected state and count/result announcement; do not encode state by color only |
| Custom select | `.js-selectBox`, `.multiselect-container` | Green menu, orange hover, generated arrow glyph | Prefer native select or an accessible listbox; no icon font |
| Listing table | `.listing-table` | Warm header `#FFF2EA`, striped white/`#F7F7F7`, orange hover | Define headers/scope, sorting, loading/empty/error and row actions |
| Responsive table | `.listing-table` mobile rules | Rows become labelled blocks below the desktop breakpoint | Preserve labels through actual markup/data attributes; never drop critical values |
| Pagination | `.pagination`, `.pagination__list`, `.pagination__input` | Number links, arrows, current state and direct page input | Label current page, disable unavailable actions and preserve URL state |
| Load more | `.js-loadmore-*` | Front/back/mobile variants and transition states | Pick either pagination or incremental loading per use case; announce added results |
| Buttons | `.btn`, `.btn--orange`, `.btn--green`, `.btn--wbg` | Square, Pragati Narrow 700; outline/default and filled variants | Use normative accessible component tokens and 44px target height |
| Text inputs | `.form-control`, `.fe-form-control` | Final override is square, borderless, `#F7F7F7`, roughly 35.6px high | Production deliberately restores border/focus and 44px minimum height |
| Checkbox/radio | `.checkbox-input`, `.radio-input`, `.rc--*` | Custom pseudo-element checks and inset shadow | Use native inputs underneath; visible focus and minimum target size |
| Validation | `.is-valid`, `.is-invalid`, feedback classes | Bootstrap green/red borders and rings | Connect error/help text with ARIA; never use color alone |
| Form groups | `.fe-form-group__label`, `__body` | Desktop split label/body percentages; stacked responsive forms | Use grid with explicit labels; stack before labels become cramped |
| Subscription form | `.subscribe-area`, `.btn-gp__input` | Orange/green promotional blocks and email action | Keep opt-in language, validation and privacy disclosure explicit |
| Contact form | contact form classes, reCAPTCHA controls | Field groups, validation and anti-abuse integration | Treat CAPTCHA as external dependency; provide failure/accessibility fallback |

## Structured-content families

| Family | Source selectors | Observed behavior | Production contract |
|---|---|---|---|
| Year accordion | `.rte-year-collapse` | Green image header, year disclosure, custom arrow; 1096px max | Native disclosure semantics, keyboard operation, state persistence where useful |
| Development timeline | `.history-year-blk` | Orange year, alternating timeline/content blocks | Use ordered data and preserve chronology without visual position dependence |
| Corporate structure | `.tree-structure`, `.node-name` | Multi-level organization chart | Provide text/list alternative and horizontal overflow at narrow widths |
| Global footprint map | `.f-map`, `.f-map__dot` | Selectable labelled locations; dark-orange selected state | Map is an enhancement; provide equivalent country/location list |
| Report/download | report/download links and cards | Annual/interim reports, PDF links and year grouping | Show file type/size/language when known; external/PDF behavior must be clear |
| Director/person | people cards and detail classes | Portrait, name/title, biography | Structured person data; respectful cropping and alt treatment |
| Job listing/detail | `.listing-table`, `.job-d__apply` | Filter/list, job metadata and apply action | Explicit status/deadline/location, accessible application route |
| News/press/e-news | list/detail, date/tag/share/related blocks | Year/category pages, article detail and downloadable releases | Shared publication primitives with schema-driven content |
| Project list/detail | media cards, gallery/content blocks | Sector list and image-led detail | Structured project metadata; responsive image strategy; no copied public assets |

## Public page-template taxonomy

This taxonomy is a consolidation aid, not a claim that all 10,666 unique content URLs were individually rendered. The audit makes three separate claims: exhaustive sitemap inventory; one real HTTP request for every locale-specific normalized content-route signature, with functionally distinct static siblings protected from `{slug}` collapsing; and responsive browser rendering of 43 route/content profiles at desktop, tablet and mobile widths. The rendered profiles include 31 detailed English profiles covering investor-relations destinations, project-sector landing pages and major list/detail/form/static route families, plus six high-value Traditional Chinese and six Simplified Chinese profiles covering home shell, group static, investor reports, publication list, project list and contact/form routes. A successful profile proves route rendering and only its non-null recorded samples; it does not prove every named function or component exists on that route. Content instances within normalized blog/job/publication families were not each visually inspected.

The sitemap, shared stylesheet, route-signature DOM audit and responsive profile walkthrough reduce the site's 10,669 entries to these reusable families:

1. **Home:** hero/key visual, announcements, project/business cards, report/download promotion and footer.
2. **Group static:** about, vision/mission/core values, corporate structure, development history, directors.
3. **Global footprint:** map plus location content.
4. **Investor relations:** landing, announcements/circulars, governance, fact sheet, financial reports, contacts, calendar, key data, stock chart and certificates.
5. **Publication listing:** news/press releases, media coverage, e-news and blog; supports year, category, tag and pagination routes.
6. **Publication detail:** title/date/tags, rich content, share/related content and optional file/video.
7. **Projects:** image-card listing and project detail.
8. **Careers:** listing/filter and job detail/application.
9. **Contact:** contact information, map and form.
10. **Legal/static:** sitemap, copyright, disclaimer and privacy policy.
11. **Document redirect:** selected press-release routes resolve directly to PDF content.

Detailed counts and normalized path signatures live in [`evidence/site-map-and-template-audit.json`](evidence/site-map-and-template-audit.json).

## Required product states

New company primitives must cover more states than the public marketing site visibly exposes:

- interactive: default, hover, focus-visible, active/pressed, disabled and pending;
- query/data: initial loading, refresh, empty, partial, error, success and unauthorized;
- forms: pristine, dirty, validating, invalid, submitting, submit failure and submit success;
- destructive: confirmation, pending, failure, completed and undo where safe;
- localization: English, Traditional Chinese and long-label stress cases;
- responsive: 390px mobile, 768px tablet, 1440px desktop and wide workspace where required;
- motion: normal and `prefers-reduced-motion`.

## Accessibility corrections versus literal source reuse

- Raw orange `#E6762D` with white normal text is 3.00:1 and is prohibited; use `#B15315` or a dark foreground.
- Replace the source's generic Bootstrap blue focus with the normative green focus treatment plus visible outline.
- Raise source form controls from roughly 35.6px to at least 44px.
- Do not make orange hover the only table-row affordance.
- Do not depend on `wico` glyphs; use approved SVG icons with accessible names.
- Preserve breadcrumb/current-location meaning when compacting mobile navigation.
- Provide list/text alternatives for maps, organization charts and image-led content.
- Carousels require pause, keyboard operation and reduced-motion handling; omit them from operational applications unless justified.
