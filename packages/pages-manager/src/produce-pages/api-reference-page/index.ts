import { getApiReferenceDescriptors } from '@lib/utils/api-reference'
import { createHead, htmlToString, withHtmlFrame } from '@lib/utils/html'
import { html } from '@remix-run/html-template'

export const produceApiReferenceIndex = (): string => {
  const head = createHead({ title: 'evidently API documentation' })
  const body = createBody()

  const page = withHtmlFrame({ head, body })

  return htmlToString(page)
}

export const createBody = () => {
  const { main, others, semvers, all } = getApiReferenceDescriptors()

  return html`
    <body>
      <main class="container">
        <a href="../" role="button" class="secondary outline" style="width: fit-content; margin-bottom: 1rem;">← Back</a>
        <article>
          <header>
            <h1>Evidently API Reference</h1>
            <h5>Browse available API documentation</h5>
          </header>
          ${all.length === 0 ? html`<p>No API reference found</p>` : ''}
          ${
            main
              ? html`
                <h6>Latest Development</h6>
                <ul>
                  <li><a href="./${main.path}">${main.displayName}</a></li>
                </ul>
              `
              : ''
          }
          ${
            semvers.length > 0
              ? html`
                <hr />
                <h6>Releases</h6>
                <ul>
                  ${semvers.map(
                    ({ path, displayName }) =>
                      html`<li>
                        <a href="./${path}">${displayName}</a>
                      </li>`
                  )}
                </ul>
              `
              : ''
          }
          ${
            others.length > 0
              ? html`
                <hr />
                <details>
                  <summary>Other API References</summary>
                  <ul>
                    ${others.map(
                      ({ path, displayName }) =>
                        html`<li>
                          <a href="./${path}">${displayName}</a>
                        </li>`
                    )}
                  </ul>
                </details>
              `
              : ''
          }
        </article>
      </main>
    </body>
`
}
