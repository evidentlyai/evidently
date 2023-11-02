import invariant from 'tiny-invariant'
import { DashboardInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = DashboardInfo

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId, testSuiteId } = params

    invariant(projectId, 'missing projectId')
    invariant(testSuiteId, 'missing testSuiteId')

    return api.getDashboard(projectId, testSuiteId)
  }
})
