import { ActionFunctionArgs } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { SnapshotInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = SnapshotInfo[]

export const injectReportsAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api.getReports(params.projectId)
  },
  action: async ({ params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')

    return api.reloadProject(params.projectId)
  }
})

export const injectTestSuitesAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api.getTestSuites(params.projectId)
  },
  action: async ({ params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')

    return api.reloadProject(params.projectId)
  }
})
