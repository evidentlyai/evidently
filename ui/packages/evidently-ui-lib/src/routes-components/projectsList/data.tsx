import { z } from 'zod'
import { API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import { ProjectModel } from '~/api/types'

import { StrictID } from '~/api/types/utils'
import { ensureID, expectJsonRequest, GetLoaderAction } from '~/api/utils'

export type LoaderData = StrictID<ProjectModel>[]

export const editProjectSchema = z.object({
  action: z.literal('edit-project')
})

export const createNewProjectSchema = z.object({
  action: z.literal('create-new-project')
})

export const deleteProjectAction = z.object({
  action: z.literal('delete-project'),
  projectId: z.string().uuid()
})

export const getLoaderAction: GetLoaderAction<API_CLIENT_TYPE, LoaderData> = ({ api }) => ({
  loader: () =>
    api
      .GET('/api/projects')
      .then(responseParser())
      .then((p) => p.map(ensureID)),

  action: async ({ request }) => {
    expectJsonRequest(request)

    // TODO: fix this (ensure submit right data in right places)
    const json = (await request.json()) as StrictID<ProjectModel>

    if (createNewProjectSchema.safeParse(json).success) {
      return api.POST('/api/projects', { body: json }).then(responseParser({ notThrowExc: true }))
    }

    const isDeleteAction = deleteProjectAction.safeParse(json)
    if (isDeleteAction.success) {
      return api
        .DELETE('/api/projects/{project_id}', {
          params: { path: { project_id: isDeleteAction.data.projectId } }
        })
        .then(responseParser({ notThrowExc: true }))
    }

    if (editProjectSchema.safeParse(json).success) {
      return api
        .POST('/api/projects/{project_id}/info', {
          params: { path: { project_id: json.id } },
          body: json
        })
        .then(responseParser({ notThrowExc: true }))
    }

    throw 'Undefined action'
  }
})
