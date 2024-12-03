import { type API, responseParser } from '~/api/client-heplers'

export const getSnapshots = ({
  api,
  projectId,
  snapshotType
}: API & { projectId: string; snapshotType: 'reports' | 'test_suites' }) =>
  api
    .GET(`/api/projects/{project_id}/${snapshotType}`, {
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
