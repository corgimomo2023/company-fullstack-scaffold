import { expect, test } from '@playwright/test'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const templateUrl = pathToFileURL(
  path.resolve(
    process.cwd(),
    '../.agents/skills/common-look-and-feel/templates/admin-cms.html',
  ),
).href

test('admin composition reference is dependency-free and responsive', async ({
  page,
}) => {
  const consoleErrors: string[] = []
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text())
  })

  for (const viewport of [
    { width: 1440, height: 1000 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport)
    await page.goto(templateUrl)

    const state = {
      pageScrollWidth: await page.evaluate<number>(
        'document.documentElement.scrollWidth',
      ),
      viewportWidth: await page.evaluate<number>('window.innerWidth'),
      navOverflow: await page.evaluate<string>(
        "getComputedStyle(document.querySelector('.nav-list')).overflowX",
      ),
      minimumControlHeight: await page.evaluate<number>(
        "Math.min(...[...document.querySelectorAll('button, input, select, .nav-link')].map((control) => control.getBoundingClientRect().height))",
      ),
      externalResources: await page.evaluate<number>(
        "[...document.querySelectorAll('link[href], script[src]')].filter((element) => /^https?:/.test(element.href || element.src)).length",
      ),
      ledeContrast: await page.evaluate<number>(
        "(() => { const channels = (value) => value.match(/[0-9.]+/g).slice(0, 3).map(Number).map((part) => part / 255); const luminance = (value) => { const rgb = channels(value).map((part) => part <= 0.04045 ? part / 12.92 : ((part + 0.055) / 1.055) ** 2.4); return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]; }; const foreground = luminance(getComputedStyle(document.querySelector('.lede')).color); const background = luminance(getComputedStyle(document.body).backgroundColor); return (Math.max(foreground, background) + 0.05) / (Math.min(foreground, background) + 0.05); })()",
      ),
    }

    expect(state.pageScrollWidth).toBeLessThanOrEqual(state.viewportWidth)
    expect(state.minimumControlHeight).toBeGreaterThanOrEqual(44)
    expect(state.externalResources).toBe(0)
    expect(state.ledeContrast).toBeGreaterThanOrEqual(4.5)
    if (viewport.width === 390) expect(state.navOverflow).toBe('auto')
  }

  await page.keyboard.press('Home')
  await page.keyboard.press('Tab')
  await expect(page.getByRole('link', { name: 'Skip to content' })).toBeFocused()
  await expect(page.getByRole('link', { name: 'Skip to content' })).toBeVisible()
  expect(consoleErrors).toEqual([])
})
