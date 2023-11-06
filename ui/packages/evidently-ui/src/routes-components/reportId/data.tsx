import invariant from 'tiny-invariant'
import { DashboardInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = DashboardInfo

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId, reportId } = params

    invariant(projectId, 'missing projectId')
    invariant(reportId, 'missing reportId')

    return api.getDashboard(projectId, reportId)
  }
})
