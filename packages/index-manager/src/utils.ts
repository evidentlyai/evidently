import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { type SafeHtml, html } from '@remix-run/html-template'
import { prettify } from 'htmlfy'

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

export const checkIsBranchFolder = (name: string) => {
  return name.startsWith('branch-')
}

export const getDisplayNameByApiReferenceFolderName = (name: string) => {
  if (checkIsBranchFolder(name)) {
    return `branch/${name.slice(7)}`
  }

  return name
}

export const consoleGroup = (message: string) => {
  console.group(`\x1b[36m${message.toUpperCase()}\x1b[0m`)
}

export const consoleGroupEnd = () => console.groupEnd()

type ApiReferenceDescriptor = {
  relativePath: string
  displayName: string
  type: 'branch' | 'main'
  fullPath: string
}

export const getApiReferenceDescriptors = (): ApiReferenceDescriptor[] => {
  if (
    !fs.existsSync(DOCS_API_REFERENCE_PATH) ||
    !fs.statSync(DOCS_API_REFERENCE_PATH).isDirectory()
  ) {
    return []
  }

  const entries = fs.readdirSync(DOCS_API_REFERENCE_PATH, { withFileTypes: true })

  return entries
    .filter((entry) => entry.isDirectory())
    .map(({ name }) => {
      const displayName = getDisplayNameByApiReferenceFolderName(name)
      const type = checkIsBranchFolder(name) ? 'branch' : 'main'
      const fullPath = join(DOCS_API_REFERENCE_PATH, name)

      return { relativePath: name, displayName, type, fullPath }
    })
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
