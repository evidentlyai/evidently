import { ActionFunctionArgs } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { GetLoaderAction } from '~/api/utils'
import { ProjectsProvider } from '~/api/types/providers/projects'
import { ReportModel, TestSuiteModel } from '~/api/types'

export type ReportsLoaderData = ReportModel[]

export const injectReportsAPI: GetLoaderAction<ProjectsProvider, ReportsLoaderData> = ({
  api
}) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api.listReports({ project: { id: params.projectId } })
  },
  action: async ({ params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')

    return api.reloadSnapshots({ project: { id: params.projectId } })
  }
})

export type TestSuitesLoaderData = TestSuiteModel[]

export const injectTestSuitesAPI: GetLoaderAction<ProjectsProvider, TestSuitesLoaderData> = ({
  api
}) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api.listTestSuites({ project: { id: params.projectId } })
  },
  action: async ({ params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')

    return api.reloadSnapshots({ project: { id: params.projectId } })
  }
})
