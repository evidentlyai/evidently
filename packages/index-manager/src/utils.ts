import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { type SafeHtml, html } from '@remix-run/html-template'
import { prettify } from 'htmlfy'
import semver from 'semver'

export const getRootPath = (): string => {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  return path.resolve(__dirname, '../../..')
}

export const join = (...segments: string[]): string => path.join(...segments)

export const DOCS_API_REFERENCE_PATH = join(getRootPath(), 'docs', 'api-reference')
export const API_REFERENCE_ARTIFACTS_PATH = join(getRootPath(), 'artifacts', 'api-reference')

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
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    />
    <title>${title}</title>
  </head>
  `

  return headTags
}

const checkIsBranchFolder = (name: string) => name.startsWith('branch-')

const trySemver = (name: string) => semver.clean(name) ?? ''

export const getReferenceType = (name: string) => {
  if (name === 'main') {
    return 'main'
  }

  if (trySemver(name)) {
    return 'semver'
  }

  if (checkIsBranchFolder(name)) {
    return 'branch'
  }

  return 'unknown'
}

export const getDisplayNameByApiReferenceFolderName = (name: string) => {
  const type = getReferenceType(name)

  if (type === 'branch') {
    return `branch/${name.slice(7)}`
  }

  return name
}

export const consoleGroup = (message: string) => {
  console.group(`\x1b[36m${message.toUpperCase()}\x1b[0m`)
}

export const consoleGroupEnd = () => console.groupEnd()

type ApiReferenceDescriptor = {
  path: string
  displayName: string
  fullPath: string
  type: 'branch' | 'main' | 'unknown' | 'semver'
  semver: string
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
      const displayName = getDisplayNameByApiReferenceFolderName(name)
      const type = getReferenceType(name)

      return { path: name, displayName, type, fullPath, semver: trySemver(name) } as const
    })

  const mainDescriptor = allEntries.find(({ type }) => type === 'main') ?? null

  const otherDescriptors = allEntries.filter(({ type }) => type === 'branch' || type === 'unknown')

  const semverDescriptors = allEntries
    .filter(({ type }) => type === 'semver')
    .sort((a, b) => -semver.compare(a.semver, b.semver))

  return {
    main: mainDescriptor,
    others: otherDescriptors,
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
