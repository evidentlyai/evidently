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
  await page.goto('/')
  await page.getByRole('link', { name: projectName, exact: true }).click()
  await page
    .getByRole('tab', { name: isTestSuite ? 'Test suites' : 'Reports', exact: true })
    .click()
  await page.getByRole('link', { name: 'View', exact: true }).first().click()
  await page.waitForLoadState('networkidle')

  const Details = page.getByRole('button', { name: 'Details', exact: true })
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
  await goToFirstSnapshotAndExpanSomeWidgets({
    page,
    projectName,
    isTestSuite
  })

  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
}

const goToSnapshotsList = async ({
  projectName,
  page,
  isTestSuite
}: {
  page: Page
  isTestSuite: boolean
  projectName: string
}) => {
  await page.goto('/')
  await page.getByRole('link', { name: projectName }).click()
  await page.getByRole('tab', { name: isTestSuite ? 'Test Suites' : 'Reports' }).click()
  await page.waitForLoadState('networkidle')
}

const VisualTestSnapshotsList = async ({
  page,
  projectName,
  isTestSuite
}: {
  page: Page
  projectName: string
  isTestSuite: boolean
}) => {
  await goToSnapshotsList({
    page,
    projectName,
    isTestSuite
  })

  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
}

const VisualTestDashboard = async ({ page, projectName }: { page: Page; projectName: string }) => {
  await page.goto('/')
  await page.getByRole('link', { name: projectName }).click()
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
}

const BikesDemoProjectName = 'Demo project - Bikes'
const ReviewsDemoProjectName = 'Demo project - Reviews'

/////////////////////
///   Home
/////////////////////

// skip due to reordering projects on home page
test.skip(`Home`, async ({ page }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
})

/////////////////////
///  Shapshots List
/////////////////////

for (const project of [BikesDemoProjectName]) {
  test(`Reports List: ${project}`, async ({ page }) => {
    await VisualTestSnapshotsList({ page, projectName: project, isTestSuite: false })
  })

  test(`Test Suites List: ${project}`, async ({ page }) => {
    await VisualTestSnapshotsList({ page, projectName: project, isTestSuite: true })
  })
}

/////////////////////
///   Dashboards
/////////////////////

for (const project of [BikesDemoProjectName, ReviewsDemoProjectName]) {
  test(`Dashboard: ${project}`, async ({ page }) => {
    await VisualTestDashboard({ page, projectName: project })
  })
}

/////////////////////
///   Snapshots
/////////////////////

for (const project of [BikesDemoProjectName, ReviewsDemoProjectName]) {
  test(`Report: ${project}`, async ({ page }) => {
    await VisualTestSnapshot({ page, projectName: project, isTestSuite: false })
  })
}

test(`Test Suite: ${BikesDemoProjectName}`, async ({ page }) => {
  await VisualTestSnapshot({ page, projectName: BikesDemoProjectName, isTestSuite: true })
})
