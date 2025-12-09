import { createHead, htmlToString, withHtmlFrame } from '@lib/utils'
import { html } from '@remix-run/html-template'

export const createBody = () => {
  return html`
    <body>
      <main class="container">
        <article>
          <header>
            <h1>Evidently</h1>
            <p>Open-source ML and LLM observability framework</p>
          </header>
          <a href="./api-reference" role="button">API Reference</a>
        </article>
      </main>
    </body>
`
}

export const produceMainIndex = (): string => {
  const head = createHead({ title: 'Evidently main' })
  const body = createBody()

  const page = withHtmlFrame({ head, body })

  return htmlToString(page)
}
