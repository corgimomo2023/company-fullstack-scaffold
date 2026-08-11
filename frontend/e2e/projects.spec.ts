import { expect, test } from '@playwright/test'

test('creates a project through the production entrypoint', async ({ page }) => {
  await page.goto('/projects')
  const projectName = `Release ${Date.now()}`
  await page.getByLabel('Project name').fill(projectName)
  await page.getByRole('button', { name: 'Create project' }).click()
  await expect(page.getByRole('list').getByText(projectName)).toBeVisible()
})
