import { AdditionalGraphInfo, DashboardAPI, WidgetInfo } from './index'

import { DashboardProvider } from './types/providers/dashboard'

export const createRemoteDashboardAPI = (dashboardProvider: DashboardProvider) => {
  return {
    getAdditionalGraphData(projectId, dashboardId, graphId) {
      return dashboardProvider.getDashboardGraph({
        project: { id: projectId },
        snapshot: { id: dashboardId },
        graph: { id: graphId }
      }) as Promise<AdditionalGraphInfo>
    },
    getAdditionalWidgetData(projectId, dashboardId, widgetId) {
      return dashboardProvider.getDashboardGraph({
        project: { id: projectId },
        snapshot: { id: dashboardId },
        graph: { id: widgetId }
      }) as Promise<WidgetInfo>
    },
    getDashboard(projectId, dashboardId) {
      return dashboardProvider.getSnapshotDashboard({
        project: { id: projectId },
        snapshot: { id: dashboardId }
      })
    }
  } satisfies DashboardAPI
}
