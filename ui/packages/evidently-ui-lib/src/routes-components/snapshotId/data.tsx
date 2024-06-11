import invariant from 'tiny-invariant'
import type { GetLoaderAction } from '~/api/utils'
import { DashboardProvider } from '~/api/types/providers/dashboard'
import { DashboardInfoModel } from '~/api/types'

export type LoaderData = DashboardInfoModel

export const getLoaderAction: GetLoaderAction<
  Pick<DashboardProvider, 'getSnapshotDashboard'>,
  LoaderData
> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId, snapshotId } = params

    invariant(projectId, 'missing projectId')
    invariant(snapshotId, 'missing testSuiteId')

    return api.getSnapshotDashboard({ project: { id: projectId }, snapshot: { id: snapshotId } })
  }
})
