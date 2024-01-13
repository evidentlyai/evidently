import { test, expect } from '@playwright/test'

test('Home screen', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveScreenshot({ fullPage: true })
})

test('Bikes Dashboard', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true })
})

test('Bikes Report', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()
  await page.getByRole('tab', { name: 'Reports' }).click()
  await page.getByRole('button', { name: 'View' }).first().click()
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true })
})

test('Bikes Test Suite', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()
  await page.getByRole('tab', { name: 'Test Suites' }).click()
  await page.getByRole('button', { name: 'View' }).first().click()
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true })
})
