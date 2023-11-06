import invariant from 'tiny-invariant'
import { ProjectDetails } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = ProjectDetails

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId } = params
    invariant(projectId, 'missing projectId')

    return api.getProjectInfo(projectId)
  }
})
