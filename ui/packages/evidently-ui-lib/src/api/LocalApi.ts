import { AdditionalGraphInfo, Api, WidgetInfo } from './index'
import { DashboardInfoModel } from './types'

export default class LocalApi implements Api {
  private readonly dashboard: DashboardInfoModel

  private additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>

  constructor(
    dashboard: DashboardInfoModel,
    additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>
  ) {
    this.dashboard = dashboard
    this.additionalGraphs = additionalGraphs
  }

  getAdditionalGraphData(
    _projectId: string,
    _dashboardId: string,
    graphId: string
  ): Promise<AdditionalGraphInfo> {
    var graph = this.additionalGraphs.get(graphId)
    return graph ? Promise.resolve(graph as AdditionalGraphInfo) : Promise.reject('No graph found')
  }

  getAdditionalWidgetData(
    _projectId: string,
    _dashboardId: string,
    widgetId: string
  ): Promise<WidgetInfo> {
    var graph = this.additionalGraphs.get(widgetId)
    return graph ? Promise.resolve(graph as WidgetInfo) : Promise.reject('No graph found')
  }

  getDashboard(_projectId: string, _dashboardId: string): Promise<DashboardInfoModel> {
    return Promise.resolve(this.dashboard)
  }
}
