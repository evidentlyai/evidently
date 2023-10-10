import {
  AdditionalGraphInfo,
  Api,
  DashboardInfo,
  ProjectDetails,
  ProjectInfo,
  ReportInfo,
  TestSuiteInfo,
  VersionInfo,
  WidgetInfo
} from './index'

export default class LocalApi implements Api {
  private readonly dashboard: DashboardInfo
  private readonly projects: ProjectInfo[]
  private additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>

  constructor(
    dashboard: DashboardInfo,
    additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>,
    projects?: ProjectInfo[]
  ) {
    this.dashboard = dashboard
    this.additionalGraphs = additionalGraphs
    this.projects = projects ?? []
  }

  async getProjectDashboard(): Promise<DashboardInfo> {
    return { name: 'Project Dasboard', widgets: [] }
  }

  async getReports(): Promise<ReportInfo[]> {
    return [{ id: 'report_1', timestamp: new Date(Date.now()).toString(), tags: [], metadata: {} }]
  }

  getAdditionalGraphData(graphId: string): Promise<AdditionalGraphInfo> {
    var graph = this.additionalGraphs.get(graphId)
    return graph ? Promise.resolve(graph as AdditionalGraphInfo) : Promise.reject('No graph found')
  }

  getAdditionalWidgetData(widgetId: string): Promise<WidgetInfo> {
    var graph = this.additionalGraphs.get(widgetId)
    return graph ? Promise.resolve(graph as WidgetInfo) : Promise.reject('No graph found')
  }

  getDashboard(): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getProjects(): Promise<ProjectInfo[]> {
    return Promise.resolve(this.projects)
  }

  getReport(): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getTestSuite(): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getTestSuites(): Promise<TestSuiteInfo[]> {
    return Promise.resolve([
      { id: 'test_suite1', timestamp: new Date(Date.now()).toString(), tags: [], metadata: {} }
    ])
  }

  getProjectInfo(): Promise<ProjectDetails> {
    return Promise.resolve({ id: 'project1', name: 'Project #1' })
  }

  getVersion(): Promise<VersionInfo> {
    return Promise.resolve({ version: 'x.x.x' })
  }
}
