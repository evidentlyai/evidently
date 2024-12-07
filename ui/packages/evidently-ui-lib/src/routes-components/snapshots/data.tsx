import { type API, responseParser } from '~/api/client-heplers'
import type { ActionSpecialArgs } from '~/router-utils/types'
import { assertNeverActionVariant } from '~/utils'

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

type ActionData =
  | {
      action: 'reload-snapshots'
      projectId: string
    }
  | {
      action: 'delete-snapshot'
      projectId: string
      snapshotId: string
    }

export const getSnapshotsActionSpecial =
  ({ api }: API) =>
  async ({ data }: ActionSpecialArgs<{ data: ActionData }>) => {
    const { action } = data

    if (action === 'reload-snapshots') {
      const { projectId } = data

      return reloadSnapshots({ api, projectId })
    }

    if (action === 'delete-snapshot') {
      const { snapshotId, projectId } = data

      return deleteSnapshot({ api, snapshotId, projectId })
    }

    assertNeverActionVariant(action)
  }
