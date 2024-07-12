import { ActionFunctionArgs } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { expectJsonRequest, GetLoaderAction } from '~/api/utils'
import { ProjectsProvider } from '~/api/types/providers/projects'
import { ReportModel, TestSuiteModel } from '~/api/types'
import { z } from 'zod'
import { ErrorData } from '~/api/types/utils'

export type ReportsLoaderData = ReportModel[]

const ACTIONS = {
  RELOAD_SNAPSHOTS: 'reload-snapshots',
  DELETE_SNAPSHOT: 'delete-snapshot'
} as const

export const reloadSnapshotSchema = z.object({
  action: z.literal(ACTIONS.RELOAD_SNAPSHOTS)
})

export const deleteSnapshotSchema = z.object({
  action: z.literal(ACTIONS.DELETE_SNAPSHOT),
  snapshotId: z.string().uuid()
})

const getAction =
  (api: ProjectsProvider) =>
  async ({ request, params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')
    expectJsonRequest(request)

    const data = await request.json()

    const reloadParse = reloadSnapshotSchema.safeParse(data)

    if (reloadParse.success) {
      return api.reloadSnapshots({ project: { id: params.projectId } })
    }

    const deleteParse = deleteSnapshotSchema.safeParse(data)

    if (deleteParse.success) {
      return api.deleteSnapshot({
        project: { id: params.projectId },
        snapshot: { id: deleteParse.data.snapshotId }
      })
    }

    return {
      error: { status_code: false, detail: 'Unknown action' }
    } satisfies ErrorData
  }

export const injectReportsAPI: GetLoaderAction<ProjectsProvider, ReportsLoaderData> = ({
  api
}) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.listReports({ project: { id: params.projectId } })
  },
  action: getAction(api)
})

export type TestSuitesLoaderData = TestSuiteModel[]

export const injectTestSuitesAPI: GetLoaderAction<ProjectsProvider, TestSuitesLoaderData> = ({
  api
}) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.listTestSuites({ project: { id: params.projectId } })
  },
  action: getAction(api)
})
