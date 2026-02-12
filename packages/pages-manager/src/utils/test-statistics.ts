import fs from 'node:fs'
import { html } from '@remix-run/html-template'
import AdmZip from 'adm-zip'
import { CI_ARTIFACTS_VARS } from './ci-artifacts'
import type { CIDescriptor } from './ci-descriptors'
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

const TYPE_TO_BADGE_MAP: Record<ArtifactTestResult['type'], string> = {
  pytest: 'pytest',
  playwright: 'UI'
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

const isTestsPassed = (testResult: ArtifactTestResult | null) => {
  return Boolean(testResult && testResult.stats.failed === 0 && testResult.stats.passed > 0)
}

export const statusBadgeForArtifact = ({ passed }: { passed: boolean }) => {
  const statusWithTextStyle = 'display: flex; align-items: center; gap: 0.25rem;'

  if (passed) {
    return html`<span style="${statusWithTextStyle}" title="All tests passed">✅ <span style="font-size: 0.85rem; color: var(--pico-color);">passed</span></span>`
  }

  return html`<span style="${statusWithTextStyle}" title="Some tests failed">❌ <span style="font-size: 0.85rem; color: var(--pico-color);">failed</span></span>`
}

export const statusBadgeForArtifacts = (artifacts: string[], fullPath: string) => {
  const testResults = artifacts.map((artifact) => {
    const htmlFilePath = join(fullPath, artifact, 'index.html')
    return extractTestStatistics(artifact, htmlFilePath)
  })

  return statusBadgeForArtifact({ passed: testResults.every(isTestsPassed) })
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
        const artifactDisplayName = artifact.replaceAll(/[_-]/g, ' ').trim()

        const statusWithText = testResult
          ? statusBadgeForArtifact({ passed: isTestsPassed(testResult) })
          : ''

        const typeBadge = testResult
          ? html`<span style="display: inline-block; padding: 0.25rem 0.5rem; background-color: var(--pico-secondary-background); color: var(--pico-secondary); border-radius: var(--pico-border-radius); font-size: 0.75rem; font-weight: 500;">${TYPE_TO_BADGE_MAP[testResult.type]}</span>`
          : ''

        const statistics = testResult
          ? [
              {
                label: 'Total',
                value: testResult.stats.total,
                color: 'var(--pico-muted-color)',
                underline: true
              },
              { label: 'Passed', value: testResult.stats.passed, color: '#28a745' },
              { label: 'Failed', value: testResult.stats.failed, color: '#dc3545' },
              { label: 'Skipped', value: testResult.stats.skipped, color: '#ffc107' }
            ].filter((stat) => stat.value > 0)
          : []

        return html`<article style="padding: 1rem; border: 1px solid var(--pico-muted-border-color); border-radius: var(--pico-border-radius); transition: transform 0.2s, box-shadow 0.2s; flex: 1 1 250px;">
            <a href="./${path}/${artifact}" style="text-decoration: none; color: inherit; display: flex; flex-direction: column; height: 100%;">
              <header style="margin-bottom: 0.5rem;">
                <hgroup style="margin-bottom: 0;">
                  <h6 style="margin-bottom: 0; font-size: 0.9rem; color: var(--pico-primary); display: flex; align-items: center; gap: 0.5rem;">
                    ${typeBadge}${artifactDisplayName} <span style="margin-left: auto;">${statusWithText}</span>
                  </h6>
                </hgroup>
              </header>
              ${
                statistics.length > 0
                  ? html`<div style="font-size: 0.85rem; display: flex; gap: 0.25rem; flex-direction: column;">
                      ${statistics.map(
                        (stat) => html`<p style="margin: 0; color: var(--pico-muted-color);">
                          <strong style="color: ${stat.color}; ${stat.underline ? 'text-decoration: underline;' : ''}">${stat.label}:</strong>
                          <span>${stat.value}</span>
                        </p>`
                      )}
                    </div>`
                  : ''
              }
              <div style="margin-top: 0.5rem; flex-grow: 1; display: flex; align-items: flex-start; flex-direction: column; justify-content: flex-end;">
              <p style="text-decoration: underline; margin: 0; font-size: 0.85rem; color: var(--pico-muted-color);">View report →</p>
              </div>
            </a>
          </article>`
      })}
    </div>
  `
}

export const makeSectionForCIDescriptors = (args: {
  title: string
  ciDescriptors: CIDescriptor[]
  includeSeparator: boolean
}) => {
  const { title, ciDescriptors, includeSeparator } = args

  if (ciDescriptors.length === 0) {
    return ''
  }

  return html`
    ${includeSeparator ? html`<hr />` : ''}
    <h4>${title}</h4>
    ${ciDescriptors.map((d, index) => {
      const prUrlComponent = d.prUrl
        ? html`<a href="${d.prUrl}" target="_blank" style="font-size: 0.85rem; text-decoration: none; color: var(--pico-primary);">🔗 View PR on GitHub</a>`
        : ''

      return html`
        ${index > 0 ? html`<hr />` : ''}
        <div id="${d.path}" style="margin-bottom: 1.5rem;">
          <div style="display: flex; flex-wrap: wrap; justify-content: flex-start; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
            <p style="margin: 0;"><strong>${d.displayName}</strong></p>
            <strong>${statusBadgeForArtifacts(d.artifacts, d.fullPath)}</strong>
            ${prUrlComponent ? html`<div style="flex: 1; display: flex; justify-content: flex-end; align-items: center;">${prUrlComponent}</div>` : ''}
          </div>
          ${renderArtifacts(d.artifacts, d.fullPath, d.path)}
        </div>
      `
    })}
  `
}
