import { type Page, expect, test } from '@playwright/test'
import { HELPERS } from './helpers'

const config = HELPERS.readConfig()

test.describe.configure({ mode: 'parallel' })

const testByName = async ({ name, page, folder }: { folder: string; name: string; page: Page }) => {
  await page.goto('/')

  await page.getByRole('link', { name: folder }).click()
  await page.getByRole('link', { name, exact: true }).click()

  await expect(page.getByRole('button').first()).toBeVisible()

  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 0 })
}

for (const [folder, files] of Object.entries(config)) {
  test.describe(folder, () => {
    for (const name of files) {
      for (const colorScheme of ['light', 'dark'] as const) {
        test.describe(name, () => {
          test.use({ colorScheme })

          test(`(${colorScheme})`, ({ page }) => testByName({ page, name, folder }))
        })
      }
    }
  })
}
