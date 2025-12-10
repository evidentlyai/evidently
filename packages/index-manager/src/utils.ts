import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { type SafeHtml, html } from '@remix-run/html-template'
import { prettify } from 'htmlfy'

export const getRootPath = (): string => {
  const __dirname = path.dirname(fileURLToPath(import.meta.url))
  return path.resolve(__dirname, '../../..')
}

export const join = (...segments: string[]): string => path.join(...segments)

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

export const getDisplayNameByApiReferenceFolderName = (name: string) => {
  if (name.startsWith('branch-')) {
    return `branch/${name.slice(7)}`
  }

  return name
}

export const consoleGroup = (message: string) => {
  console.group(`\x1b[36m${message.toUpperCase()}\x1b[0m`)
}

export const consoleGroupEnd = () => console.groupEnd()
