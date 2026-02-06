import { getCIDescriptors } from '@lib/utils/ci-descriptors'
import { createHead, htmlToString, withHtmlFrame } from '@lib/utils/html'
import { renderArtifacts } from '@lib/utils/test-statistics'
import { html } from '@remix-run/html-template'

export const produceCIIndex = (): string => {
  const head = createHead({ title: 'evidently CI Reports' })
  const body = createBody()

  const page = withHtmlFrame({ head, body })

  return htmlToString(page)
}

export const createBody = () => {
  const { main, prs, branches, all } = getCIDescriptors()

  return html`
    <body>
      <style>
        h4,
        div[id] {
          scroll-margin-top: 1rem;
        }
        h4:target,
        div[id]:target {
          outline: 2px solid var(--pico-primary);
          outline-offset: 5px;
          border-radius: 4px;
        }
      </style>
      <main class="container">
        <a href="../" role="button" class="secondary outline" style="width: fit-content; margin-bottom: 1rem;">← Back</a>
        <article style="padding:2rem;">
          <header style="padding: 2rem;">
            <h1>Evidently CI Reports</h1>
            <h5>Browse available CI artifacts and test reports</h5>
          </header>
          ${all.length === 0 ? html`<p>No CI reports found</p>` : ''}
          ${
            main
              ? html`
                <h4>Latest Development</h4>
                <div id="${main.path}" style="margin-bottom: 1.5rem;">
                  <p style="margin-bottom: 0.5rem;">
                    <strong>${main.displayName}</strong>
                  </p>
                  ${renderArtifacts(main.artifacts, main.fullPath, main.path)}
                </div>
              `
              : ''
          }
          ${
            prs.length > 0
              ? html`
                <hr />
                <h4>Pull Requests</h4>
                ${prs.map(
                  ({ path, displayName, artifacts, fullPath }) =>
                    html`<div id="${path}" style="margin-bottom: 1.5rem;">
                      <p style="margin-bottom: 0.5rem;">
                        <strong>${displayName}</strong>
                      </p>
                      ${renderArtifacts(artifacts, fullPath, path)}
                    </div>`
                )}
              `
              : ''
          }
          ${
            branches.length > 0
              ? html`
                <hr />
                <h4>Branches</h4>
                ${branches.map(
                  ({ path, displayName, artifacts, fullPath }) =>
                    html`<div id="${path}" style="margin-bottom: 1.5rem;">
                      <p style="margin-bottom: 0.5rem;">
                        <strong>${displayName}</strong>
                      </p>
                      ${renderArtifacts(artifacts, fullPath, path)}
                    </div>`
                )}
              `
              : ''
          }
        </article>
      </main>
      <script>
        if (typeof anchors !== 'undefined') {
          anchors.options = {placement: 'left', icon: '#'};
          anchors.add('h4, div[id]');
        }
      </script>
    </body>
`
}
