import { type SafeHtml, html } from '@remix-run/html-template'
import { prettify } from 'htmlfy'

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
