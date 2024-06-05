import { z } from 'zod'
import { ProjectModel } from '~/api/types'
import { ProjectsProvider } from '~/api/types/providers/projects'
import { StrictID } from '~/api/types/utils'
import { GetLoaderAction, expectJsonRequest } from '~/utils'

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

export const getLoaderAction: GetLoaderAction<
  Pick<ProjectsProvider, 'create' | 'delete' | 'update' | 'list'>,
  LoaderData
> = ({ api }) => ({
  loader: () => api.list(),
  action: async ({ request }) => {
    expectJsonRequest(request)

    const json = (await request.json()) as StrictID<ProjectModel>

    if (createNewProjectSchema.safeParse(json).success) {
      return api.create({ body: json })
    }

    const isDeleteAction = deleteProjectAction.safeParse(json)
    if (isDeleteAction.success) {
      return api.delete({ id: isDeleteAction.data.projectId })
    }

    if (editProjectSchema.safeParse(json).success) {
      return api.update({ body: json })
    }

    throw 'Undefined action'
  }
})
