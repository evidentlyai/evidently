import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { type SafeHtml, html } from '@remix-run/html-template'
import AdmZip from 'adm-zip'
import { prettify } from 'htmlfy'
import semver from 'semver'

export const getRootPath = (): string => {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  return path.resolve(__dirname, '../../..')
}

export const join = (...segments: string[]): string => path.join(...segments)

export const DOCS_API_REFERENCE_PATH = join(getRootPath(), 'docs', 'api-reference')
export const ARTIFACTS_PATH = join(getRootPath(), 'artifacts')
export const API_REFERENCE_ARTIFACTS_PATH = join(ARTIFACTS_PATH, 'api-reference')

export const CI_ARTIFACTS_VARS = {
  UI_SERVICE_PLAYWRIGHT_REPORT: 'ui-service-playwright-report',
  UI_HTML_VISUAL_TESTING_PLAYWRIGHT_REPORT: 'ui-html-visual-testing-playwright-report',
  PYTEST_HTML_REPORT: 'pytest-html-report'
} as const

export const CI_ARTIFACTS = [
  CI_ARTIFACTS_VARS.UI_SERVICE_PLAYWRIGHT_REPORT,
  CI_ARTIFACTS_VARS.UI_HTML_VISUAL_TESTING_PLAYWRIGHT_REPORT,
  CI_ARTIFACTS_VARS.PYTEST_HTML_REPORT
] as const

export type CIArtifact = (typeof CI_ARTIFACTS)[number]

export const DOCS_CI_PATH = join(getRootPath(), 'docs', 'ci')

type HtmlFrameArgs = { head: SafeHtml; body: SafeHtml }

export const withHtmlFrame = (args: HtmlFrameArgs) => {
  const { head, body } = args

  return html`
    <!DOCTYPE html>
    <html lang="en">
    ${head}
    ${body}
    </html>
`
}

export const htmlToString = (html: SafeHtml, makePretty = true) => {
  const htmlString = String(html)

  if (makePretty) {
    return `${prettify(htmlString)}\n`
  }

  return htmlString
}

type CreateHeadArgs = {
  title: string
}

export const createHead = (args: CreateHeadArgs) => {
  const { title } = args

  const headTags = html`
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="https://demo.evidentlyai.com/favicon.ico"/>
    <link rel="preload" as="image" href="https://demo.evidentlyai.com/static/img/evidently-ai-logo.png">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    />
    <script src="https://cdn.jsdelivr.net/npm/anchor-js@5.0.0/anchor.min.js"></script>
    <title>${title}</title>
  </head>
  `

  return headTags
}

const checkIsPRAndBranch = (name: string) => name.startsWith('pr-')
const trySemver = (name: string) => semver.clean(name) ?? ''

export const getReferenceType = (name: string) => {
  if (name === 'main') {
    return 'main'
  }

  if (trySemver(name)) {
    return 'semver'
  }

  if (checkIsPRAndBranch(name)) {
    return 'pr-and-branch'
  }

  return 'unknown'
}

const extractPRNumber = (name: string) => {
  const type = getReferenceType(name)

  if (type !== 'pr-and-branch') {
    return { number: 0, rest: name }
  }

  const [_, number, ...rest] = name.split('-')

  return { number: Number.parseInt(number), rest: rest.join('-') }
}

export const getDisplayName = (name: string) => {
  const type = getReferenceType(name)

  if (type === 'pr-and-branch') {
    const { number, rest } = extractPRNumber(name)
    return `PR ${number} (${rest})`
  }

  return name
}

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[36m',
  blue: '\x1b[34m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  orange: '\x1b[38;5;208m',
  red: '\x1b[31m',
  magenta: '\x1b[35m',
  gray: '\x1b[90m'
} as const

export const consoleGroup = (message: string) => {
  console.group(`${colors.blue}${colors.bright}${message.toUpperCase()}${colors.reset}`)
}

export const consoleGroupEnd = () => console.groupEnd()

export const colorize = {
  branch: (text: string) => `${colors.cyan}${colors.bright}${text}${colors.reset}`,
  time: (text: string) => `${colors.yellow}${text}${colors.reset}`,
  date: (text: string) => `${colors.gray}${text}${colors.reset}`,
  deleted: (text: string) => `${colors.red}${colors.bright}✓ ${text}${colors.reset}`,
  kept: (text: string) => `${colors.green}${colors.dim}→ ${text}${colors.reset}`,
  age: (days: number) => {
    if (days < 1) return `${colors.green}${days}${colors.reset}`
    if (days < 3) return `${colors.yellow}${days}${colors.reset}`
    if (days < 7) return `${colors.orange}${days}${colors.reset}`
    return `${colors.red}${days}${colors.reset}`
  }
}

type ApiReferenceDescriptor = {
  path: string
  displayName: string
  fullPath: string
  type: 'main' | 'unknown' | 'semver' | 'pr-and-branch'
  semver: string
  prNumber: number
}

export const getApiReferenceDescriptors = (): {
  all: ApiReferenceDescriptor[]
  main: ApiReferenceDescriptor | null
  others: ApiReferenceDescriptor[]
  semvers: ApiReferenceDescriptor[]
} => {
  if (
    !fs.existsSync(DOCS_API_REFERENCE_PATH) ||
    !fs.statSync(DOCS_API_REFERENCE_PATH).isDirectory()
  ) {
    return { all: [], main: null, others: [], semvers: [] }
  }

  const entries = fs.readdirSync(DOCS_API_REFERENCE_PATH, { withFileTypes: true })

  const allEntries = entries
    .filter((entry) => entry.isDirectory())
    .map(({ name }) => {
      const fullPath = join(DOCS_API_REFERENCE_PATH, name)
      const displayName = getDisplayName(name)
      const type = getReferenceType(name)

      return {
        path: name,
        displayName,
        type,
        fullPath,
        semver: trySemver(name),
        prNumber: extractPRNumber(name).number
      } as const
    })

  const mainDescriptor = allEntries.find(({ type }) => type === 'main') ?? null

  const prAndBranchDescriptors = allEntries
    .filter(({ type }) => type === 'pr-and-branch')
    .sort((a, b) => b.prNumber - a.prNumber)

  const unknownDescriptors = allEntries.filter(({ type }) => type === 'unknown')

  const semverDescriptors = allEntries
    .filter(({ type }) => type === 'semver')
    .sort((a, b) => -semver.compare(a.semver, b.semver))

  return {
    main: mainDescriptor,
    others: [...prAndBranchDescriptors, ...unknownDescriptors],
    semvers: semverDescriptors,
    all: allEntries
  }
}

type FolderLastModificationTimestamp = {
  lastModificationTimestamp: number
  lastModificationDateString: string
}

export const getFolderLastModificationTimestamp = (
  folderPath: string
): FolderLastModificationTimestamp | null => {
  const gitOptions = { encoding: 'utf-8', stdio: 'pipe' } as const

  try {
    const output = execSync(
      `git -C "${getRootPath()}" log -1 --format=%ct -- "${folderPath}"`,
      gitOptions
    ).trim()

    if (!output) return null

    const commitTime = Number.parseInt(output, 10)
    if (Number.isNaN(commitTime)) return null

    const lastModificationTimestamp = commitTime * 1000
    const lastModificationDateString = new Date(lastModificationTimestamp).toString()

    return { lastModificationTimestamp, lastModificationDateString }
  } catch {
    console.error(`Error getting last modification timestamp for ${folderPath}`)
    return null
  }
}

type CIDescriptor = {
  path: string
  displayName: string
  fullPath: string
  artifacts: string[]
  prNumber: number
  isPR: boolean
}

export const getCIDescriptors = (): {
  all: CIDescriptor[]
  main: CIDescriptor | null
  prs: CIDescriptor[]
  branches: CIDescriptor[]
} => {
  if (!fs.existsSync(DOCS_CI_PATH) || !fs.statSync(DOCS_CI_PATH).isDirectory()) {
    return { all: [], main: null, prs: [], branches: [] }
  }

  const entries = fs.readdirSync(DOCS_CI_PATH, { withFileTypes: true })

  const allDescriptors = entries
    .filter((entry) => entry.isDirectory())
    .map(({ name }) => {
      const fullPath = join(DOCS_CI_PATH, name)
      const subfolderEntries = fs.readdirSync(fullPath, { withFileTypes: true })

      const artifacts = subfolderEntries
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)

      const type = getReferenceType(name)
      const isPR = type === 'pr-and-branch'
      const prNumber = extractPRNumber(name).number
      const displayName = getDisplayName(name)

      return {
        path: name,
        displayName,
        fullPath,
        artifacts,
        prNumber,
        isPR
      }
    })

  const mainDescriptor = allDescriptors.find(({ path }) => path === 'main') ?? null

  const prDescriptors = allDescriptors
    .filter(({ isPR }) => isPR)
    .sort((a, b) => b.prNumber - a.prNumber)

  const branchDescriptors = allDescriptors.filter(({ isPR, path }) => !isPR && path !== 'main')

  return {
    all: allDescriptors,
    main: mainDescriptor,
    prs: prDescriptors,
    branches: branchDescriptors
  }
}

type TestStatistics = {
  total: number
  passed: number
  failed: number
  skipped: number
}

type ArtifactTestResult = {
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

    // Extract the JSON blob from the data-jsonblob attribute
    const jsonBlobMatch = htmlContent.match(/data-jsonblob="([^"]*)"/)
    if (!jsonBlobMatch || !jsonBlobMatch[1]) {
      console.error('Could not find data-jsonblob attribute in HTML file')
      return null
    }

    // Decode HTML entities (e.g., &#34; -> ")
    const decodedJson = jsonBlobMatch[1]
      .replace(/&#34;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')

    // Parse the JSON
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

  // Extract the base64 encoded zip from window.playwrightReportBase64
  const base64Match = htmlContent.match(
    /window\.playwrightReportBase64\s*=\s*"data:application\/zip;base64,([^"]+)"/
  )
  if (!base64Match || !base64Match[1]) {
    console.error('Could not find playwrightReportBase64 in HTML file')
    return null
  }

  // Decode base64 to buffer
  const zipBuffer = Buffer.from(base64Match[1], 'base64')

  const zip = new AdmZip(zipBuffer)

  // Find the report.json file in the zip
  const reportEntry = zip.getEntry('report.json') || zip.getEntry('data/report.json')
  if (!reportEntry) {
    console.error('Could not find report.json in playwright zip')
    return null
  }

  // Extract and parse the JSON
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

  // Use the stats object from the report which already has aggregated counts
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
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1rem; margin-top: 0.5rem;">
      ${artifacts.map((artifact, index) => {
        const testResult = testResults[index]

        const statusIcon =
          testResult && testResult.stats.failed === 0
            ? html`<span style="font-size: 1.1rem; margin-left: 0.5rem;" title="All tests passed">✅</span>`
            : testResult && testResult.stats.failed > 0
              ? html`<span style="font-size: 1.1rem; margin-left: 0.5rem;" title="Some tests failed">❌</span>`
              : ''

        return html`<article style="padding: 1rem; border: 1px solid var(--pico-muted-border-color); border-radius: var(--pico-border-radius); transition: transform 0.2s, box-shadow 0.2s;">
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
