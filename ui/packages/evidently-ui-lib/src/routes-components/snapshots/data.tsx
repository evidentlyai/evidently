import { ActionFunctionArgs } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { expectJsonRequest, GetLoaderAction } from '~/api/utils'
import { ReportModel, TestSuiteModel } from '~/api/types'
import { z } from 'zod'
import { ErrorData } from '~/api/types/utils'
import { API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'

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
  (api: API_CLIENT_TYPE) =>
  async ({ request, params }: ActionFunctionArgs) => {
    invariant(params.projectId, 'missing projectId')
    expectJsonRequest(request)

    const data = await request.json()

    const reloadParse = reloadSnapshotSchema.safeParse(data)

    if (reloadParse.success) {
      return api
        .GET('/api/projects/{project_id}/reload', {
          params: { path: { project_id: params.projectId } }
        })
        .then(responseParser({ notThrowExc: true }))
    }

    const deleteParse = deleteSnapshotSchema.safeParse(data)

    if (deleteParse.success) {
      return api
        .DELETE('/api/projects/{project_id}/{snapshot_id}', {
          params: {
            path: { project_id: params.projectId, snapshot_id: deleteParse.data.snapshotId }
          }
        })
        .then(responseParser({ notThrowExc: true }))
    }

    return {
      error: { status_code: false, detail: 'Unknown action' }
    } satisfies ErrorData
  }

export const injectReportsAPI: GetLoaderAction<API_CLIENT_TYPE, ReportsLoaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api
      .GET('/api/projects/{project_id}/reports', {
        params: { path: { project_id: params.projectId } }
      })
      .then(responseParser())
  },
  action: getAction(api)
})

export type TestSuitesLoaderData = TestSuiteModel[]

export const injectTestSuitesAPI: GetLoaderAction<API_CLIENT_TYPE, TestSuitesLoaderData> = ({
  api
}) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    if (params.snapshotId) {
      return Promise.resolve([])
    }

    return api
      .GET('/api/projects/{project_id}/test_suites', {
        params: { path: { project_id: params.projectId } }
      })
      .then(responseParser())
  },
  action: getAction(api)
})
