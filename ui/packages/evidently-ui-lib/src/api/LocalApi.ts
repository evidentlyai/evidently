import {
  AdditionalGraphInfo,
  Api,
  DashboardInfo,
  ProjectDetails,
  ProjectInfo,
  SnapshotInfo,
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

  async getProjectDashboard(
    _projectId: string,
    _from?: string,
    _to?: string
  ): Promise<DashboardInfo> {
    return {
      name: 'Project Dasboard',
      widgets: [],
      min_timestamp: new Date(Date.now()).toString(),
      max_timestamp: new Date(Date.now()).toString()
    }
  }
  async getReports(_projectId: string): Promise<SnapshotInfo[]> {
    return [{ id: 'report_1', timestamp: new Date(Date.now()).toString(), tags: [], metadata: {} }]
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

  getDashboard(_projectId: string, _dashboardId: string): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getProjects(): Promise<ProjectInfo[]> {
    return Promise.resolve(this.projects)
  }

  getReport(_projectId: string, _reportId: string): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getTestSuite(_projectId: string, _reportId: string): Promise<DashboardInfo> {
    return Promise.resolve(this.dashboard)
  }

  getTestSuites(_projectId: string): Promise<SnapshotInfo[]> {
    return Promise.resolve([
      { id: 'test_suite1', timestamp: new Date(Date.now()).toString(), tags: [], metadata: {} }
    ])
  }

  getProjectInfo(_projectId: string): Promise<ProjectDetails> {
    return Promise.resolve({ id: 'project1', name: 'Project #1' })
  }

  getVersion(): Promise<VersionInfo> {
    return Promise.resolve({ version: 'x.x.x' })
  }

  editProjectInfo(_project: ProjectDetails) {
    return Promise.resolve(new Response('ok', { status: 200 }))
  }
}
