import { test, expect } from '@playwright/test'

test('Has title', async ({ page }) => {
  await page.goto('/')

  await expect(page).toHaveTitle(/Evidently/)
})

// We don't need this since visual testing enabled
test.skip('Can view Snapshot', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()
  await page.getByText('Bike Rental Demand Forecast').click()
  await page.getByRole('tab', { name: 'Reports' }).click()

  await expect(page.getByRole('columnheader', { name: 'Report ID' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Tags' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Timestamp' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Actions' })).toBeVisible()

  await page.getByRole('link', { name: 'View' }).first().click()
  await expect(page.getByText('Dataset Drift', { exact: true })).toBeVisible()

  await page.getByRole('tab', { name: 'Test suites' }).click()

  await expect(page.getByRole('columnheader', { name: 'Test Suite ID' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Tags' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Timestamp' })).toBeVisible()
  await expect(page.getByRole('columnheader', { name: 'Actions' })).toBeVisible()

  await page.getByRole('link', { name: 'View' }).first().click()
  await expect(page.getByText('Drift per Column', { exact: true }).first()).toBeVisible()
})

test('Download reports', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()

  await page.waitForLoadState('domcontentloaded')

  for (const tab of ['Reports']) {
    await page.getByRole('tab', { name: tab }).click()

    for (const downloadType of ['Download HTML', 'Download JSON']) {
      await page.getByText('Download').first().click()

      const downloadPromise = page.waitForEvent('download')

      await page.getByRole('menuitem', { name: downloadType }).click()

      const download = await downloadPromise

      expect(await download.failure()).toBeNull()
    }
  }
})

test('Download test suites', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()

  await page.waitForLoadState('domcontentloaded')

  for (const tab of ['Test Suites']) {
    await page.getByRole('tab', { name: tab }).click()

    for (const downloadType of ['Download HTML', 'Download JSON']) {
      await page.getByText('Download').first().click()

      const downloadPromise = page.waitForEvent('download')

      await page.getByRole('menuitem', { name: downloadType }).click()

      const download = await downloadPromise

      expect(await download.failure()).toBeNull()
    }
  }
})

// We don't need this since visual testing enabled
test.skip('We expect to see at least 3 plotly graphs', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()
  for (let index = 0; index < 3; index++) {
    await expect(page.locator('.js-plotly-plot').nth(index)).toBeVisible()
  }
})

test('Filter Reports and Test Suites by tags', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()

  for (const [tab, columnName] of [
    ['Reports', 'Report ID'],
    ['Test Suites', 'Test Suite ID']
  ]) {
    await page.getByRole('tab', { name: tab }).click()
    await expect(page.getByRole('columnheader', { name: columnName })).toBeVisible()

    const rowsNumberBeforeFiltration = await page.getByRole('row').count()

    await page
      .getByRole('button', { name: /high_seasonality|production_critical|tabular_data/ })
      .first()
      .click()

    const rowsNumberAfterFiltration = await page.getByRole('row').count()

    // console.log(
    //   'rowsNumberBeforeFiltration, rowsNumberAfterFiltration',
    //   rowsNumberBeforeFiltration,
    //   rowsNumberAfterFiltration
    // )

    expect(rowsNumberBeforeFiltration).toBeGreaterThan(rowsNumberAfterFiltration)
  }
})

test('Altering project title and description', async ({ page }) => {
  await page.goto('/')

  await expect(page.getByText('Project List')).toBeVisible()

  await page.getByRole('link', { name: 'Demo project - Reviews' }).hover()

  await page
    .getByText(
      'Demo project - ReviewsA toy demo project using E-commerce Reviews dataset. Text and tabular data, classification.'
    )
    .getByTestId('EditIcon')
    .click()

  await page.locator('input[name="name"]').fill('Reviews new title')
  await page.locator('input[name="description"]').fill('Reviews new description')

  await page.getByText('Save').click()

  await page.waitForLoadState('domcontentloaded')

  await expect(page.getByText('Reviews new title')).toBeVisible()
  await expect(page.getByText('Reviews new description')).toBeVisible()

  await page.getByRole('link', { name: 'Reviews new title' }).hover()

  await page.getByText('Reviews new titleReviews new description').getByTestId('EditIcon').click()

  await page.locator('input[name="name"]').fill('Demo project - Reviews')
  await page
    .locator('input[name="description"]')
    .fill(
      'A toy demo project using E-commerce Reviews dataset. Text and tabular data, classification.'
    )

  await page.getByText('Save').click()

  await page.waitForLoadState('domcontentloaded')
})

// We don't need this since visual testing enabled
test.skip('Check header of ColumnSummaryMetric', async ({ page }) => {
  const expectedHeaderCells = ['', 'current', 'reference']

  await page.goto('/')
  await page.getByRole('link', { name: 'Home', exact: true }).click()
  await page.getByRole('link', { name: 'Demo project - Reviews', exact: true }).click()
  await page.getByRole('tab', { name: 'Reports', exact: true }).click()
  await page.getByRole('link', { name: 'View', exact: true }).first().click()
  const graph = await page.getByText('OOVnumcurrentreference')
  await expect(graph).toBeVisible()

  const actualHeaderCells = await graph.locator('thead tr th').allInnerTexts()

  for (let i = 0; i < expectedHeaderCells.length; i++) {
    expect(expectedHeaderCells[i] === actualHeaderCells[i], {
      message: `expected: "${expectedHeaderCells[i]}", actual: "${actualHeaderCells[i]}"`
    }).toBeTruthy()
  }
})
