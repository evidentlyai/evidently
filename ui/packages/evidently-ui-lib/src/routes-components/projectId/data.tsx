import { type API, responseParser } from '~/api/client-heplers'

import { ensureID } from '~/api/utils'

export const getProjectInfo = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/info', { params: { path: { project_id: projectId } } })
    .then(responseParser())
    .then(ensureID)
    .then((project) => ({ project }))
