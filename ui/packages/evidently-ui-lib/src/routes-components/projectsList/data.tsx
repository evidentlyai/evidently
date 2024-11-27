import { type API, responseParser } from '~/api/client-heplers'
import type { ProjectModel } from '~/api/types'

import type { StrictID } from '~/api/types/utils'
import { ensureIDInArray } from '~/api/utils'

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
