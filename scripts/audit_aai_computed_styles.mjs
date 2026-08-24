#!/usr/bin/env node

import { createRequire } from 'node:module'
import { createHash } from 'node:crypto'
import { mkdir, writeFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

import {
  applyBrowserNetworkPolicy,
  browserContextOptions,
} from './aai_browser_network_policy.mjs'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const requireFromFrontend = createRequire(resolve(ROOT, 'frontend/package.json'))
const { chromium } = requireFromFrontend('@playwright/test')

const OUTPUT = resolve(
  ROOT,
  process.argv[2] ?? 'docs/design-system/evidence/computed-style-walkthrough.json',
)

const profiles = [
  ['home', 'https://www.asiaalliedgroup.com/en'],
  ['group-about', 'https://www.asiaalliedgroup.com/en/the-group/about-the-group'],
  ['group-vision', 'https://www.asiaalliedgroup.com/en/the-group/vision-mission-and-core-values'],
  ['corporate-structure', 'https://www.asiaalliedgroup.com/en/corporate-structure'],
  ['development-history', 'https://www.asiaalliedgroup.com/en/development-history'],
  ['global-footprint', 'https://www.asiaalliedgroup.com/en/global-footprint'],
  ['projects-list', 'https://www.asiaalliedgroup.com/en/projects'],
  ['project-bus-services', 'https://www.asiaalliedgroup.com/en/projects/bus-services-business'],
  ['project-construction', 'https://www.asiaalliedgroup.com/en/projects/construction'],
  ['project-healthcare', 'https://www.asiaalliedgroup.com/en/projects/medical-technology-and-healthcare'],
  ['project-other-business', 'https://www.asiaalliedgroup.com/en/projects/other-business'],
  ['project-professional-services', 'https://www.asiaalliedgroup.com/en/projects/professional-services'],
  ['project-property', 'https://www.asiaalliedgroup.com/en/projects/property-development-and-assets-leasing'],
  ['investor-announcements', 'https://www.asiaalliedgroup.com/en/investor-relations/announcements-circulars'],
  ['investor-governance', 'https://www.asiaalliedgroup.com/en/investor-relations/corporate-governance'],
  ['investor-fact-sheet', 'https://www.asiaalliedgroup.com/en/investor-relations/fact-sheet'],
  ['investor-reports', 'https://www.asiaalliedgroup.com/en/investor-relations/financial-reports'],
  ['investor-contacts', 'https://www.asiaalliedgroup.com/en/investor-relations/investor-contacts'],
  ['investor-overview', 'https://www.asiaalliedgroup.com/en/investor-relations/investor-relations'],
  ['investor-calendar', 'https://www.asiaalliedgroup.com/en/investor-relations/ir-calendar'],
  ['investor-key-data', 'https://www.asiaalliedgroup.com/en/investor-relations/key-financial-data'],
  ['investor-lost-certificates', 'https://www.asiaalliedgroup.com/en/investor-relations/replacement-of-lost-share-certificates'],
  ['investor-stock-chart', 'https://www.asiaalliedgroup.com/en/investor-relations/stock-chart'],
  ['investor-welcome', 'https://www.asiaalliedgroup.com/en/investor-relations/welcome-page'],
  ['publication-list', 'https://www.asiaalliedgroup.com/en/press-release'],
  ['publication-detail', 'https://www.asiaalliedgroup.com/en/blog/from-construction-2-0-to-the-year-of-ai-innovations-inspired-by-s960'],
  ['blog-list', 'https://www.asiaalliedgroup.com/en/blog'],
  ['career-list', 'https://www.asiaalliedgroup.com/en/career'],
  ['career-detail', 'https://www.asiaalliedgroup.com/en/career/accountant-construction-j2022082203'],
  ['contact-form', 'https://www.asiaalliedgroup.com/en/contact-us'],
  ['legal-static', 'https://www.asiaalliedgroup.com/en/privacy-policy'],
  ['tc-home', 'https://www.asiaalliedgroup.com/tc'],
  ['tc-group-about', 'https://www.asiaalliedgroup.com/tc/the-group/about-the-group'],
  ['tc-investor-reports', 'https://www.asiaalliedgroup.com/tc/investor-relations/financial-reports'],
  ['tc-publication-list', 'https://www.asiaalliedgroup.com/tc/press-release'],
  ['tc-projects-list', 'https://www.asiaalliedgroup.com/tc/projects'],
  ['tc-contact-form', 'https://www.asiaalliedgroup.com/tc/contact-us'],
  ['sc-home', 'https://www.asiaalliedgroup.com/sc'],
  ['sc-group-about', 'https://www.asiaalliedgroup.com/sc/the-group/about-the-group'],
  ['sc-investor-reports', 'https://www.asiaalliedgroup.com/sc/investor-relations/financial-reports'],
  ['sc-publication-list', 'https://www.asiaalliedgroup.com/sc/press-release'],
  ['sc-projects-list', 'https://www.asiaalliedgroup.com/sc/projects'],
  ['sc-contact-form', 'https://www.asiaalliedgroup.com/sc/contact-us'],
]

const profileFilter = process.env.AAI_PROFILE_FILTER
const selectedProfiles = profileFilter
  ? profiles.filter(([name]) => name === profileFilter)
  : profiles
if (profileFilter && selectedProfiles.length === 0) {
  throw new Error(`Unknown AAI_PROFILE_FILTER: ${profileFilter}`)
}

const viewports = [
  ['desktop', { width: 1440, height: 900 }],
  ['tablet', { width: 768, height: 900 }],
  ['mobile', { width: 390, height: 844 }],
]

const probes = {
  body: 'body',
  header: '.page-head, header',
  desktopNavigation: '.mn__nav, nav',
  mobileNavigation: '.mb-mn__wrap, .mTrigger__open',
  breadcrumb: '.breadcrumb',
  pageTitle: '.page-title, main h1, h1',
  contentHeading: 'main h2, main h3',
  paragraph: 'main p',
  button: '.btn, main button, input[type="submit"]',
  tag: '.tag',
  card: '.img-card-blk, .img-title-blk, .top-img-blk, .img-blog-blk, .thumb-blk',
  pageTabs: '.blk-tab__btn, .tab__select',
  filterBar: '.filter',
  informationTile: '.it-blk',
  imageSlider: '.image-slider',
  milestone: '.milestone-blk',
  shareDropdown: '.link-copy-dropdown',
  input: 'main input:not([type="hidden"]), main textarea',
  select: 'main select, .js-selectBox',
  table: '.listing-table, main table',
  footer: 'footer',
}

const styleProperties = [
  'display',
  'visibility',
  'position',
  'color',
  'backgroundColor',
  'fontFamily',
  'fontSize',
  'fontWeight',
  'lineHeight',
  'letterSpacing',
  'textTransform',
  'width',
  'maxWidth',
  'minHeight',
  'margin',
  'padding',
  'gap',
  'border',
  'borderRadius',
  'boxShadow',
  'opacity',
]

async function firstVisible(page, selector, { requireEnabled = false } = {}) {
  const candidates = page.locator(selector)
  for (let attempt = 0; attempt < 2; attempt += 1) {
    try {
      const index = await candidates.evaluateAll(
        (elements, enabledRequired) =>
          elements.slice(0, 200).findIndex((element) => {
            const style = getComputedStyle(element)
            const rect = element.getBoundingClientRect()
            const disabled =
              element.matches(':disabled') || element.getAttribute('aria-disabled') === 'true'
            const visible =
              !element.hidden &&
              style.display !== 'none' &&
              style.visibility !== 'hidden' &&
              rect.width > 0 &&
              rect.height > 0
            return visible && (!enabledRequired || (!disabled && style.pointerEvents !== 'none'))
          }),
        requireEnabled,
      )
      return index >= 0 ? candidates.nth(index) : null
    } catch (error) {
      const navigationRace = `${error}`.includes('Execution context was destroyed')
      if (!navigationRace || attempt > 0) throw error
      await page.waitForLoadState('domcontentloaded', { timeout: 10_000 })
      await page.waitForTimeout(500)
      if (new URL(page.url()).origin !== 'https://www.asiaalliedgroup.com') {
        throw new Error(`Cross-origin retry URL blocked: ${page.url()}`)
      }
    }
  }
  return null
}

async function sample(locator) {
  return locator.evaluate((element, properties) => {
    const style = getComputedStyle(element)
    const rect = element.getBoundingClientRect()
    const disabled =
      element.matches(':disabled') || element.getAttribute('aria-disabled') === 'true'
    const visible =
      !element.hidden &&
      style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      rect.width > 0 &&
      rect.height > 0
    const values = Object.fromEntries(properties.map((property) => [property, style[property]]))
    return {
      tag: element.tagName.toLowerCase(),
      id: element.id || null,
      classes: [...element.classList].slice(0, 8),
      text: (element.textContent ?? '').replace(/\s+/g, ' ').trim().slice(0, 120),
      hidden: element.hidden,
      visible,
      disabled,
      interactive: visible && !disabled && style.pointerEvents !== 'none',
      ariaDisabled: element.getAttribute('aria-disabled'),
      values,
    }
  }, styleProperties)
}

async function captureState(page, selector, state) {
  const requireEnabled = ['hover', 'focus', 'active'].includes(state)
  const locator = await firstVisible(page, selector, { requireEnabled })
  if (!locator) return null
  try {
    if (state === 'inspect') {
      return { evidenceMethod: 'computed-style-static-state-observation', ...(await sample(locator)) }
    }
    if (state === 'hover') await locator.hover({ timeout: 2_000 })
    if (state === 'focus') {
      await locator.focus({ timeout: 2_000 })
      const focused = await locator.evaluate((element) => document.activeElement === element)
      if (!focused) return null
    }
    if (state === 'active') {
      const box = await locator.boundingBox()
      if (!box) return null
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2)
      await page.mouse.down()
      try {
        return {
          evidenceMethod: 'computed-style-while-pointer-active',
          ...(await sample(locator)),
        }
      } finally {
        await page.mouse.up()
      }
    }
    return { evidenceMethod: `computed-style-${state}`, ...(await sample(locator)) }
  } catch {
    return null
  }
}

const browser = await chromium.launch({ headless: true })
const results = []
const failures = []

try {
  for (const [profile, url] of selectedProfiles) {
    if (new URL(url).origin !== 'https://www.asiaalliedgroup.com') {
      throw new Error(`Out-of-scope profile URL blocked: ${url}`)
    }
    for (const [viewportName, viewport] of viewports) {
      const locale = url.includes('/tc') ? 'zh-HK' : url.includes('/sc') ? 'zh-CN' : 'en-HK'
      const context = await browser.newContext(browserContextOptions({ viewport, locale }))
      await applyBrowserNetworkPolicy(context, 'https://www.asiaalliedgroup.com')
      const page = await context.newPage()
      try {
        const response = await page.goto(url, {
          waitUntil: 'domcontentloaded',
          timeout: 30_000,
        })
        if (new URL(page.url()).origin !== 'https://www.asiaalliedgroup.com') {
          throw new Error(`Cross-origin final URL blocked: ${page.url()}`)
        }
        await page.evaluate(async () => {
          if (document.fonts?.ready) await document.fonts.ready
        })
        await page.waitForTimeout(250)

        const styles = {}
        for (const [name, selector] of Object.entries(probes)) {
          const locator = await firstVisible(page, selector)
          styles[name] = locator ? await sample(locator) : null
        }

        const stateCandidates = {
          buttonHover: await captureState(page, probes.button, 'hover'),
          buttonFocus: await captureState(page, probes.button, 'focus'),
          buttonActive: await captureState(page, probes.button, 'active'),
          buttonDisabled: await captureState(
            page,
            'button:disabled, input[type="submit"]:disabled, .btn[aria-disabled="true"]',
            'inspect',
          ),
          tagHover: await captureState(page, probes.tag, 'hover'),
          tagSelected: await captureState(page, '.tag.selected, .tag.active', 'inspect'),
          cardHover: await captureState(page, probes.card, 'hover'),
          cardFocus: await captureState(
            page,
            '.img-card-blk a, .img-title-blk a, .top-img-blk a, .img-blog-blk a, .thumb-blk a',
            'focus',
          ),
          inputFocus: await captureState(page, probes.input, 'focus'),
          inputDisabled: await captureState(
            page,
            'main input:disabled, main textarea:disabled, main select:disabled',
            'inspect',
          ),
          tabActive: await captureState(page, '.blk-tab__btn.active', 'inspect'),
        }
        const states = Object.fromEntries(
          Object.entries(stateCandidates).filter(([, evidence]) => evidence !== null),
        )

        const html = await page.content()
        const dimensions = await page.evaluate(() => ({
          bodyScrollWidth: document.body.scrollWidth,
          documentClientWidth: document.documentElement.clientWidth,
        }))
        results.push({
          profile,
          requestedUrl: url,
          finalUrl: page.url(),
          viewport: { name: viewportName, ...viewport },
          status: response?.status() ?? null,
          title: await page.title(),
          htmlSha256: createHash('sha256').update(html).digest('hex'),
          ...dimensions,
          horizontalOverflow: dimensions.bodyScrollWidth > dimensions.documentClientWidth + 1,
          styles,
          states,
        })
      } catch (error) {
        failures.push({
          profile,
          url,
          viewport: viewportName,
          error: `${error.name}: ${error.message}`,
        })
      } finally {
        await context.close()
      }
    }
  }
} finally {
  await browser.close()
}

const output = {
  schemaVersion: 2,
  auditDate: '2026-08-19',
  methodology:
    'Computed-style walkthrough of protected English static-route families plus consolidated content-route profiles and high-value Traditional/Simplified Chinese shell, static, list, project and form routes at desktop, tablet and mobile viewports. A successful profile/viewport record proves page rendering and only the non-null samples recorded from visible elements within it; it does not prove that every named function or component exists on that route. Hover/focus/pointer-active samples additionally require a visible enabled actionable element, and unsuccessful states are omitted rather than stored as null records. This complements exhaustive sitemap discovery and representative HTTP/DOM coverage; it does not imply manual browser inspection of every sitemap URL.',
  networkScope:
    'Every profile, redirect and browser subresource is restricted to the exact https://www.asiaalliedgroup.com origin; data/blob resources are allowed and all other origins are blocked.',
  sourceOwnership:
    'Values are factual evidence from the public site. No CSS, fonts, images, marks or copy are vendored or relicensed.',
  profiles: selectedProfiles.map(([name, url]) => ({ name, url })),
  viewports: viewports.map(([name, value]) => ({ name, ...value })),
  resultCount: results.length,
  failureCount: failures.length,
  failures,
  results,
}

await mkdir(dirname(OUTPUT), { recursive: true })
await writeFile(OUTPUT, `${JSON.stringify(output, null, 2)}\n`, 'utf8')
console.log(
  JSON.stringify(
    {
      output: OUTPUT,
      profiles: selectedProfiles.length,
      viewports: viewports.length,
      results: results.length,
      failures: failures.length,
    },
    null,
    2,
  ),
)
process.exitCode = failures.length === 0 ? 0 : 1
