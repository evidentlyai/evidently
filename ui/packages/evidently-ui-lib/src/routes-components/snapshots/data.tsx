import invariant from 'tiny-invariant'
import { SnapshotInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = SnapshotInfo[]

export const injectReportsAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.getReports(params.projectId)
  }
})

export const injectTestSuitesAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.getTestSuites(params.projectId)
  }
})
