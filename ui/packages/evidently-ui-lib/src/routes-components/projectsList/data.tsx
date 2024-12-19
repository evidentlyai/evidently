import { type API, responseParser } from '~/api/client-heplers'
import type { ProjectModel } from '~/api/types'

import type { StrictID } from '~/api/types/utils'
import { ensureIDInArray } from '~/api/utils'
import type { ActionSpecialArgs } from '~/router-utils/types'

export const getProjects = ({ api }: API) =>
  api.GET('/api/projects').then(responseParser()).then(ensureIDInArray)

export const editProject = ({ api, project }: API & { project: StrictID<ProjectModel> }) =>
  api
    .POST('/api/projects/{project_id}/info', {
      params: { path: { project_id: project.id } },
      body: project
    })
    .then(responseParser({ notThrowExc: true }))

export const deleteProject = ({ api, project_id }: API & { project_id: string }) =>
  api
    .DELETE('/api/projects/{project_id}', { params: { path: { project_id } } })
    .then(responseParser({ notThrowExc: true }))

type CreateProjectParams = { project: ProjectModel }

export const createProject = ({ api, project }: API & CreateProjectParams) =>
  api
    .POST('/api/projects', {
      body: project,
      params: { query: { team_id: project.team_id ?? undefined } }
    })
    .then(responseParser({ notThrowExc: true }))

export const getProjectsListActions = ({ api }: API) => ({
  'delete-project': (args: ActionSpecialArgs<{ data: { project_id: string } }>) =>
    deleteProject({ api, project_id: args.data.project_id }),
  'create-project': (args: ActionSpecialArgs<{ data: { project: ProjectModel } }>) =>
    createProject({ api, project: args.data.project }),
  'edit-project': (args: ActionSpecialArgs<{ data: { project: StrictID<ProjectModel> } }>) =>
    editProject({ api, project: args.data.project })
})
