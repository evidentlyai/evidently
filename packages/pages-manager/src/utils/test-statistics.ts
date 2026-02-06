import fs from 'node:fs'
import { html } from '@remix-run/html-template'
import AdmZip from 'adm-zip'
import { CI_ARTIFACTS_VARS } from './ci-artifacts'
import { join } from './paths'

export type TestStatistics = {
  total: number
  passed: number
  failed: number
  skipped: number
}

export type ArtifactTestResult = {
  type: 'pytest' | 'playwright'
  stats: TestStatistics
}

const detectArtifactType = (artifactName: string): 'pytest' | 'playwright' | null => {
  if (artifactName === CI_ARTIFACTS_VARS.PYTEST_HTML_REPORT) {
    return 'pytest'
  }

  if (
    artifactName.includes(CI_ARTIFACTS_VARS.UI_SERVICE_PLAYWRIGHT_REPORT) ||
    artifactName.includes(CI_ARTIFACTS_VARS.UI_HTML_VISUAL_TESTING_PLAYWRIGHT_REPORT)
  ) {
    return 'playwright'
  }

  return null
}

const extractPytestStatistics = (htmlFilePath: string): TestStatistics | null => {
  try {
    const htmlContent = fs.readFileSync(htmlFilePath, 'utf-8')

    const jsonBlobMatch = htmlContent.match(/data-jsonblob="([^"]*)"/)
    if (!jsonBlobMatch || !jsonBlobMatch[1]) {
      console.error('Could not find data-jsonblob attribute in HTML file')
      return null
    }

    const decodedJson = jsonBlobMatch[1]
      .replace(/&#34;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')

    const jsonData = JSON.parse(decodedJson) as {
      tests?: Record<string, Array<{ result?: string }>>
    }

    const tests = jsonData.tests ?? {}
    const total = Object.keys(tests).length
    const passed = Object.values(tests).filter(
      (testList) => testList?.[0]?.result === 'Passed'
    ).length
    const failed = Object.values(tests).filter(
      (testList) => testList?.[0]?.result === 'Failed'
    ).length
    const skipped = Object.values(tests).filter(
      (testList) => testList?.[0]?.result === 'Skipped'
    ).length

    return { total, passed, failed, skipped }
  } catch (error) {
    console.error(`Error extracting pytest test statistics: ${error}`)
    return null
  }
}

const extractPlaywrightStatistics = (htmlFilePath: string): TestStatistics | null => {
  if (!fs.existsSync(htmlFilePath)) {
    console.error(`Playwright HTML report not found: ${htmlFilePath}`)
    return null
  }

  const htmlContent = fs.readFileSync(htmlFilePath, 'utf-8')

  const base64Match = htmlContent.match(
    /window\.playwrightReportBase64\s*=\s*"data:application\/zip;base64,([^"]+)"/
  )
  if (!base64Match || !base64Match[1]) {
    console.error('Could not find playwrightReportBase64 in HTML file')
    return null
  }

  const zipBuffer = Buffer.from(base64Match[1], 'base64')

  const zip = new AdmZip(zipBuffer)

  const reportEntry = zip.getEntry('report.json') || zip.getEntry('data/report.json')
  if (!reportEntry) {
    console.error('Could not find report.json in playwright zip')
    return null
  }

  const reportJson = zip.readAsText(reportEntry)
  const reportData = JSON.parse(reportJson) as {
    stats?: {
      total?: number
      expected?: number
      unexpected?: number
      flaky?: number
      skipped?: number
    }
  }

  const stats = reportData.stats
  if (!stats) {
    console.error('Could not find stats in playwright report')
    return null
  }

  const total = stats.total ?? 0
  const passed = (stats.expected ?? 0) + (stats.flaky ?? 0)
  const failed = stats.unexpected ?? 0
  const skipped = stats.skipped ?? 0

  return { total, passed, failed, skipped }
}

export const extractTestStatistics = (
  artifactName: string,
  htmlFilePath: string
): ArtifactTestResult | null => {
  if (!fs.existsSync(htmlFilePath)) {
    console.error(`HTML report not found: ${htmlFilePath}`)
    return null
  }

  const type = detectArtifactType(artifactName)
  if (!type) return null

  const stats =
    type === 'pytest'
      ? extractPytestStatistics(htmlFilePath)
      : type === 'playwright'
        ? extractPlaywrightStatistics(htmlFilePath)
        : null

  if (!stats) return null

  return { type, stats }
}

export const renderArtifacts = (artifacts: string[], fullPath: string, path: string) => {
  if (artifacts.length === 0) {
    return ''
  }

  const testResults = artifacts.map((artifact) => {
    const htmlFilePath = join(fullPath, artifact, 'index.html')
    return extractTestStatistics(artifact, htmlFilePath)
  })

  return html`
    <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 0.5rem;">
      ${artifacts.map((artifact, index) => {
        const testResult = testResults[index]

        const statusIcon =
          testResult && testResult.stats.failed === 0
            ? html`<span style="font-size: 1.1rem; margin-left: 0.5rem;" title="All tests passed">✅</span>`
            : testResult && testResult.stats.failed > 0
              ? html`<span style="font-size: 1.1rem; margin-left: 0.5rem;" title="Some tests failed">❌</span>`
              : ''

        return html`<article style="padding: 1rem; border: 1px solid var(--pico-muted-border-color); border-radius: var(--pico-border-radius); transition: transform 0.2s, box-shadow 0.2s; flex: 1 1 250px;">
            <a href="./${path}/${artifact}" style="text-decoration: none; color: inherit; display: block;">
              <header style="margin-bottom: 0.5rem;">
                <hgroup style="margin-bottom: 0;">
                  <h6 style="margin-bottom: 0; font-size: 0.9rem; color: var(--pico-primary); display: flex; align-items: center;">
                    ${artifact}${statusIcon}
                  </h6>
                </hgroup>
              </header>
              ${
                testResult
                  ? html`<div style="margin-top: 0.5rem; font-size: 0.85rem;">
                  <p style="margin: 0.25rem 0; color: var(--pico-muted-color);">
                    <strong style="text-decoration: underline;">Total:</strong> ${testResult.stats.total}
                  </p>
                  <p style="margin: 0.25rem 0; color: var(--pico-muted-color);">
                  <strong style="color: #28a745;">Passed:</strong> ${testResult.stats.passed}
                  </p>
                  <p style="margin: 0.25rem 0; color: var(--pico-muted-color);">
                  <strong style="color: #dc3545;">Failed:</strong> ${testResult.stats.failed}
                  </p>
                  ${
                    testResult.stats.skipped > 0
                      ? html`<p style="margin: 0.25rem 0; color: var(--pico-muted-color);">
                    <strong style="color: #ffc107;">Skipped:</strong> ${testResult.stats.skipped}
                    </p>`
                      : ''
                  }
                  </div>`
                  : ''
              }
              <p style="margin: 0; font-size: 0.85rem; color: var(--pico-muted-color);">View report →</p>
            </a>
          </article>`
      })}
    </div>
  `
}
