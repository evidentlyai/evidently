import { type API, responseParser } from '~/api/client-heplers'
import type { ActionSpecialArgs } from '~/router-utils/types'

export const getReports = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/reports', {
      params: { path: { project_id: projectId } }
    })
    .then(responseParser())

export const getTestSuites = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/test_suites', {
      params: { path: { project_id: projectId } }
    })
    .then(responseParser())

export const reloadSnapshots = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/reload', {
      params: { path: { project_id: projectId } }
    })
    .then(responseParser({ notThrowExc: true }))

export const deleteSnapshot = ({
  api,
  projectId,
  snapshotId
}: API & { projectId: string; snapshotId: string }) =>
  api
    .DELETE('/api/projects/{project_id}/{snapshot_id}', {
      params: { path: { project_id: projectId, snapshot_id: snapshotId } }
    })
    .then(responseParser({ notThrowExc: true }))

export const getSnapshotsActionSpecial = ({ api }: API) => ({
  'reload-snapshots': ({
    data: { projectId }
  }: ActionSpecialArgs<{ data: { projectId: string } }>) => reloadSnapshots({ api, projectId }),
  'delete-snapshot': ({
    data: { snapshotId, projectId }
  }: ActionSpecialArgs<{ data: { snapshotId: string; projectId: string } }>) =>
    deleteSnapshot({ api, snapshotId, projectId })
})
