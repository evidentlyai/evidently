import { AdditionalGraphInfo, WidgetInfo } from '~/api'
import { DashboardInfoModel } from '~/api/types'
import { ID } from '~/api/types/utils'

export type DashboardProvider = {
  getProjectDashboard(args: {
    project: ID
    options: {
      timestamp_start?: null | string
      timestamp_end?: null | string
    }
  }): Promise<DashboardInfoModel>

  getSnapshotDashboard(args: { project: ID; snapshot: ID }): Promise<DashboardInfoModel>

  getDashboardGraph(args: {
    project: ID
    snapshot: ID
    graph: ID
  }): Promise<AdditionalGraphInfo | WidgetInfo>
}
