import { JSONParseExtended } from '~/api/JsonParser'
import { type API, responseParser } from '~/api/client-heplers'
import type { DashboardInfoModel } from '~/api/types'

export const getSnapshotInfo = ({
  api,
  projectId,
  snapshotId
}: API & { projectId: string; snapshotId: string }) =>
  api
    .GET('/api/projects/{project_id}/{snapshot_id}/data', {
      params: { path: { project_id: projectId, snapshot_id: snapshotId } },
      parseAs: 'text'
    })
    .then(responseParser())
    .then(JSONParseExtended<DashboardInfoModel>)
