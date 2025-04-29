import { type Page, expect, test } from '@playwright/test'

const goToFirstSnapshotAndExpanSomeWidgets = async ({
  projectName,
  page
}: {
  page: Page

  projectName: string
}) => {
  await page.goto('/')
  await page.getByRole('link', { name: projectName, exact: true }).click()
  await page.getByRole('tab', { name: 'Reports', exact: true }).click()
  await page.getByRole('link', { name: 'View', exact: true }).first().click()
  await page.waitForLoadState('networkidle')

  const Details = page.getByRole('button', { name: 'Details', exact: true })

  const DetailsCount = await Details.count()

  if (DetailsCount === 0) {
    return
  }

  await expect(Details.first()).toBeVisible()

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
  projectName
}: {
  page: Page
  projectName: string
}) => {
  await goToFirstSnapshotAndExpanSomeWidgets({
    page,
    projectName
  })

  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
}

const goToSnapshotsList = async ({
  projectName,
  page
}: {
  page: Page
  projectName: string
}) => {
  await page.goto('/')
  await page.getByRole('link', { name: projectName }).click()
  await page.getByRole('tab', { name: 'Reports' }).click()
  await page.waitForLoadState('networkidle')
}

const VisualTestSnapshotsList = async ({
  page,
  projectName
}: {
  page: Page
  projectName: string
}) => {
  await goToSnapshotsList({
    page,
    projectName
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

/////////////////////
///   Home
/////////////////////

test('Home', async ({ page }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')
  await expect(page).toHaveScreenshot({ fullPage: true, maxDiffPixels: 150 })
})

/////////////////////
///  Shapshots List
/////////////////////

for (const project of [BikesDemoProjectName]) {
  test(`Reports List: ${project}`, async ({ page }) => {
    await VisualTestSnapshotsList({ page, projectName: project })
  })
}

/////////////////////
///   Dashboards
/////////////////////

for (const project of [BikesDemoProjectName]) {
  test(`Dashboard: ${project}`, async ({ page }) => {
    await VisualTestDashboard({ page, projectName: project })
  })
}

/////////////////////
///   Snapshots
/////////////////////

for (const project of [BikesDemoProjectName]) {
  test(`Report: ${project}`, async ({ page }) => {
    await VisualTestSnapshot({ page, projectName: project })
  })
}
