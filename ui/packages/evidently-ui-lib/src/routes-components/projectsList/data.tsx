import { type API, responseParser } from '~/api/client-heplers'
import type { ProjectModel } from '~/api/types'

import type { StrictID } from '~/api/types/utils'
import { ensureIDInArray } from '~/api/utils'
import type { ActionArgs } from '~/router-utils/types'

export const getProjects = ({ api }: API) =>
  api.GET('/api/projects').then(responseParser()).then(ensureIDInArray)

export const getProjectsListActions = ({ api }: API) => ({
  'delete-project': (args: ActionArgs<{ data: { project_id: string } }>) =>
    api
      .DELETE('/api/projects/{project_id}', {
        params: { path: { project_id: args.data.project_id } }
      })
      .then(responseParser({ notThrowExc: true })),
  'create-project': (
    args: ActionArgs<{ data: { project: ProjectModel; orgId?: string | null } }>
  ) =>
    api
      .POST('/api/projects', {
        body: args.data.project,
        params: { query: { org_id: args.data.orgId } }
      })
      .then(responseParser({ notThrowExc: true })),
  'edit-project': (args: ActionArgs<{ data: { project: StrictID<ProjectModel> } }>) =>
    api
      .POST('/api/projects/{project_id}/info', {
        params: { path: { project_id: args.data.project.id } },
        body: args.data.project
      })
      .then(responseParser({ notThrowExc: true }))
})
