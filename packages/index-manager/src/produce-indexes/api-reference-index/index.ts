import { createHead, getApiReferenceDescriptors, htmlToString, withHtmlFrame } from '@lib/utils'
import { html } from '@remix-run/html-template'

export const produceApiReferenceIndex = (): string => {
  const head = createHead({ title: 'Evidently API reference' })
  const body = createBody()

  const page = withHtmlFrame({ head, body })

  return htmlToString(page)
}

export const createBody = () => {
  const apiReferenceDescriptors = getApiReferenceDescriptors()

  const mainDescriptors = apiReferenceDescriptors.filter(({ type }) => type === 'main')
  const otherDescriptors = apiReferenceDescriptors.filter(({ type }) => type === 'branch')

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
                    ${mainDescriptors.map(({ relativePath, displayName }) => html`<p><a href="./${relativePath}">${displayName}</a></p>`)}
                  `
                  : ''
              }
              ${
                otherDescriptors.length > 0
                  ? html`
                    <details>
                      <summary>Other api references</summary>
                      <ul>
                        ${otherDescriptors.map(({ relativePath, displayName }) => html`<li><a href="./${relativePath}">${displayName}</a></li>`)}
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
