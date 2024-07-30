import invariant from 'tiny-invariant'
import type { GetLoaderAction } from '~/api/utils'
import { DashboardInfoModel } from '~/api/types'
import { API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import { JSONParseExtended } from '~/api/JsonParser'

export type LoaderData = DashboardInfoModel

export const getLoaderAction: GetLoaderAction<API_CLIENT_TYPE, LoaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId, snapshotId } = params

    invariant(projectId, 'missing projectId')
    invariant(snapshotId, 'missing testSuiteId')

    return api
      .GET('/api/projects/{project_id}/{snapshot_id}/data', {
        params: { path: { project_id: projectId, snapshot_id: snapshotId } },
        parseAs: 'text'
      })
      .then(responseParser())
      .then(JSONParseExtended<DashboardInfoModel>)
  }
})
