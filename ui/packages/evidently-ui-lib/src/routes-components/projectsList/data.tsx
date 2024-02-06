import { z } from 'zod'
import { ProjectInfo } from '~/api'
import { InJectAPI, expectJsonRequest } from '~/utils'

export type loaderData = ProjectInfo[]

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

    const isCreateAction = createNewProjectSchema.safeParse(json)
    if (isCreateAction.success && isCreateAction.data.action === 'create-new-project') {
      return api.createProject(json)
    }

    const isDeleteAction = deleteProjectAction.safeParse(json)
    if (isDeleteAction.success && isDeleteAction.data.action === 'delete-project') {
      return api.deleteProject(isDeleteAction.data.projectId)
    }

    return api.editProjectInfo(json)
  }
})
