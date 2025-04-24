import { type API, responseParser } from '~/api/client-heplers'
import type { ActionArgs } from '~/router-utils/types'

export const getReports = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/snapshots', {
      params: { path: { project_id: projectId } }
    })
    .then(responseParser())

export const getTestSuites = ({ api, projectId }: API & { projectId: string }) =>
  api
    .GET('/api/projects/{project_id}/test_suites', {
      params: { path: { project_id: projectId } }
    })
    .then(responseParser())

export const getSnapshotsActions = ({ api }: API) => ({
  'reload-snapshots': (args: ActionArgs<{ data: { projectId: string } }>) =>
    api
      .GET('/api/projects/{project_id}/reload', {
        params: { path: { project_id: args.data.projectId } }
      })
      .then(responseParser({ notThrowExc: true })),
  'delete-snapshot': (args: ActionArgs<{ data: { snapshotId: string; projectId: string } }>) =>
    api
      .DELETE('/api/projects/{project_id}/{snapshot_id}', {
        params: { path: { project_id: args.data.projectId, snapshot_id: args.data.snapshotId } }
      })
      .then(responseParser({ notThrowExc: true }))
})
