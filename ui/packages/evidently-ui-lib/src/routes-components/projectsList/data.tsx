import { z } from 'zod'
import { ProjectInfo } from '~/api'
import { InJectAPI, expectJsonRequest } from '~/utils'

export type loaderData = ProjectInfo[]

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

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: () => api.getProjects(),
  action: async ({ request }) => {
    expectJsonRequest(request)

    const json = await request.json()

    if (createNewProjectSchema.safeParse(json).success) {
      return api.createProject(json)
    }

    const isDeleteAction = deleteProjectAction.safeParse(json)
    if (isDeleteAction.success) {
      return api.deleteProject(isDeleteAction.data.projectId)
    }

    if (editProjectSchema.safeParse(json).success) {
      return api.editProjectInfo(json)
    }

    throw 'Undefined action'
  }
})
