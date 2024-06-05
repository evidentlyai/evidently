import { DashboardAPI } from './index'

import { DashboardProvider } from './types/providers/dashboard'

export const createRemoteDashboardAPI = (dashboardProvider: DashboardProvider) => {
  return {
    getAdditionalGraphData(projectId, dashboardId, graphId) {
      return dashboardProvider.getDashboardGraph({
        project: { id: projectId },
        snapshot: { id: dashboardId },
        graph: { id: graphId }
      })
    },
    getAdditionalWidgetData(projectId, dashboardId, widgetId) {
      return dashboardProvider.getDashboardGraph({
        project: { id: projectId },
        snapshot: { id: dashboardId },
        graph: { id: widgetId }
      })
    },
    getDashboard(projectId, dashboardId) {
      return dashboardProvider.getSnapshotDashboard({
        project: { id: projectId },
        snapshot: { id: dashboardId }
      })
    }
  } satisfies DashboardAPI
}
