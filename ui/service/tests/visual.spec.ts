import { test, expect, Page } from '@playwright/test'

const goToFirstSnapshotAndExpanSomeWidgets = async ({
  projectName,
  page,
  isTestSuite
}: {
  page: Page
  isTestSuite: boolean
  projectName: string
}) => {
  await page.getByRole('link', { name: projectName }).click()
  await page.getByRole('tab', { name: isTestSuite ? 'Test Suites' : 'Reports' }).click()
  await page.getByRole('button', { name: 'View' }).first().click()
  await page.waitForLoadState('networkidle')

  const Details = page.getByRole('button', { name: 'Details' })
  await expect(Details.first()).toBeVisible()

  const DetailsCount = await Details.count()

  await Details.first().click()
  await page.waitForLoadState('networkidle')

  if (DetailsCount > 1) {
    await Details.nth(1).click()
    await page.waitForLoadState('networkidle')
  }

  if (DetailsCount > 2) {
    await Details.last().click()
    await page.waitForLoadState('networkidle')
  }

  await page.waitForTimeout(1000)
}

const VisualTestSnapshot = async ({
  page,
  projectName,
  isTestSuite
}: {
  page: Page
  projectName: string
  isTestSuite: boolean
}) => {
  await page.goto('/')
  await goToFirstSnapshotAndExpanSomeWidgets({
    page,
    projectName,
    isTestSuite
  })

  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 1800 })
}

const VisualTestDashboard = async ({ page, projectName }: { page: Page; projectName: string }) => {
  await page.goto('/')
  await page.getByRole('link', { name: projectName }).click()
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 800 })
}

const BikesDemoProjectName = 'Demo project - Bikes'
const ReviewsDemoProjectName = 'Demo project - Reviews'

/////////////////////
///   Dashboards
/////////////////////
test(`${BikesDemoProjectName}: Dashboard`, async ({ page }) => {
  await VisualTestDashboard({ page, projectName: BikesDemoProjectName })
})

test(`${ReviewsDemoProjectName}: Dashboard`, async ({ page }) => {
  await VisualTestDashboard({ page, projectName: ReviewsDemoProjectName })
})

/////////////////////
///   Snapshots
/////////////////////
test(`${BikesDemoProjectName}: Report`, async ({ page }) => {
  await VisualTestSnapshot({ page, projectName: BikesDemoProjectName, isTestSuite: false })
})

test(`${BikesDemoProjectName}: Test Suite`, async ({ page }) => {
  await VisualTestSnapshot({ page, projectName: BikesDemoProjectName, isTestSuite: true })
})

test(`${ReviewsDemoProjectName}: Report`, async ({ page }) => {
  await VisualTestSnapshot({ page, projectName: ReviewsDemoProjectName, isTestSuite: false })
})
