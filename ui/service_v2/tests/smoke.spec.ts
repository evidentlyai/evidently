import { expect, test } from '@playwright/test'

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
  await expect(page.getByText('Dataset Summary', { exact: true })).toBeVisible()
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

test('Filter Reports by tags', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('link', { name: 'Demo project - Bikes' }).click()

  for (const [tab, columnName] of [['Reports', 'Report ID']]) {
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

  await page.getByRole('link', { name: 'Demo project - Bikes' }).hover()

  await page
    .getByText('Demo project - BikesA toy demo project using Bike Demand forecasting dataset')
    .getByTestId('EditIcon')
    .click()

  await page.locator('input[name="name"]').fill('Bikes new title')
  await page.locator('input[name="description"]').fill('Bikes new description')

  await page.getByText('Save').click()

  await page.waitForLoadState('domcontentloaded')

  await expect(page.getByText('Bikes new title')).toBeVisible()
  await expect(page.getByText('Bikes new description')).toBeVisible()

  await page.getByRole('link', { name: 'Bikes new title' }).hover()

  await page.getByText('Bikes new titleBikes new description').getByTestId('EditIcon').click()

  await page.locator('input[name="name"]').fill('Demo project - Bikes')
  await page
    .locator('input[name="description"]')
    .fill('A toy demo project using Bike Demand forecasting dataset')

  await page.getByText('Save').click()

  await page.waitForLoadState('domcontentloaded')
})
