import fs from 'node:fs'

import {
  createHead,
  getDisplayNameByApiReferenceFolderName,
  getRootPath,
  htmlToString,
  join,
  withHtmlFrame
} from '@lib/utils'
import { html } from '@remix-run/html-template'

export const produceApiReferenceIndex = (): string => {
  const head = createHead({ title: 'Evidently API reference' })
  const body = createBody()

  const page = withHtmlFrame({ head, body })

  return htmlToString(page)
}

export const createBody = () => {
  const apiReferencePath = join(getRootPath(), 'docs', 'api-reference')

  const apiReferenceDescriptors: { path: string; displayName: string }[] = (() => {
    if (!fs.existsSync(apiReferencePath) || !fs.statSync(apiReferencePath).isDirectory()) {
      return []
    }

    const entries = fs.readdirSync(apiReferencePath, { withFileTypes: true })

    return entries
      .filter((entry) => entry.isDirectory())
      .map(({ name }) => {
        const displayName = getDisplayNameByApiReferenceFolderName(name)
        return { path: name, displayName }
      })
  })()

  const mainDescriptors = apiReferenceDescriptors.filter(({ path }) => path === 'main')
  const otherDescriptors = apiReferenceDescriptors.filter(({ path }) => path !== 'main')

  return html`
    <body>
      <main class="container">
        <a href="../" role="button" class="secondary outline" style="width: fit-content; margin-bottom: 1rem;">← Back</a>
        <article>
          <header>
            <h1>Evidently API Reference</h1>
            <h5>Browse available API documentation</h5>
          </header>
          ${
            apiReferenceDescriptors.length > 0
              ? html`
              ${
                mainDescriptors.length > 0
                  ? html`
                    ${mainDescriptors.map(({ path, displayName }) => html`<p><a href="./${path}">${displayName}</a></p>`)}
                  `
                  : ''
              }
              ${
                otherDescriptors.length > 0
                  ? html`
                    <details>
                      <summary>Other api references</summary>
                      <ul>
                        ${otherDescriptors.map(({ path, displayName }) => html`<li><a href="./${path}">${displayName}</a></li>`)}
                      </ul>
                    </details>
                  `
                  : ''
              }
            `
              : html`<p>No API reference found</p>`
          }
        </article>
      </main>
    </body>
`
}
