import { type API, responseParser } from '~/api/client-heplers'
import type { ProjectModel } from '~/api/types'

import type { StrictID } from '~/api/types/utils'
import { ensureIDInArray } from '~/api/utils'
import type { ActionSpecialArgs } from '~/router-utils/types'
import { assertNeverActionVariant } from '~/utils'

export const getProjects = ({ api }: API) =>
  api.GET('/api/projects').then(responseParser()).then(ensureIDInArray)

export const editProject = ({ api, project }: API & { project: StrictID<ProjectModel> }) =>
  api
    .POST('/api/projects/{project_id}/info', {
      params: { path: { project_id: project.id } },
      body: project
    })
    .then(responseParser({ notThrowExc: true }))
    .then((d) => (d && 'error' in d ? d : null))

export const deleteProject = ({ api, project_id }: API & { project_id: string }) =>
  api
    .DELETE('/api/projects/{project_id}', { params: { path: { project_id } } })
    .then(responseParser({ notThrowExc: true }))
    .then((d) => (d && 'error' in d ? d : null))

type CreateProjectParams = { project: ProjectModel }

export const createProject = ({ api, project }: API & CreateProjectParams) =>
  api
    .POST('/api/projects', {
      body: project,
      params: { query: { team_id: project.team_id ?? undefined } }
    })
    .then(responseParser({ notThrowExc: true }))
    .then((d) => (d && 'error' in d ? d : null))

type ActionRequestData =
  | { action: 'delete-project'; project_id: string }
  | { action: 'edit-project'; project: StrictID<ProjectModel> }
  | { action: 'create-project'; project: ProjectModel }

export const getProjectsListActionSpecial =
  ({ api }: API) =>
  async ({ data }: ActionSpecialArgs<{ data: ActionRequestData }>) => {
    const { action } = data

    if (action === 'delete-project') {
      return deleteProject({ api, project_id: data.project_id })
    }

    if (action === 'edit-project') {
      return editProject({ api, project: data.project })
    }

    if (action === 'create-project') {
      return createProject({ api, project: data.project })
    }

    assertNeverActionVariant(action)
  }
