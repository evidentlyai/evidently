import { DashboardInfoModel } from '~/api/types'
import { ID, StrictID } from '~/api/types/utils'

export type DashboardProvider = {
  getProjectDashboard(args: {
    project: ID
    options: {
      timestamp_start?: null | string
      timestamp_end?: null | string
    }
  }): Promise<StrictID<DashboardInfoModel>>

  getSnapshotDashboard(args: { project: ID; snapshot: ID }): Promise<StrictID<DashboardInfoModel>>
  getDashboardGraph(args: { project: ID; snapshot: ID; graph: ID }): Promise<any>
}
