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

class JsonParser {
  parse(rawJson: string) {
    return JSON.parse(rawJson)
  }
}

export class RemoteApi implements Api {
  private readonly endpoint: string

  public constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  async getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string) {
    const resp = await fetch(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${graphId}`
    )
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as AdditionalGraphInfo
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getAdditionalWidgetData(
    projectId: string,
    dashboardId: string,
    widgetId: string
  ): Promise<WidgetInfo> {
    const resp = await fetch(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${widgetId}`
    )
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as WidgetInfo
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getDashboard(projectId: string, dashboardId: string) {
    const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`)
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as DashboardInfo
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getProjects() {
    const resp = await fetch(`${this.endpoint}/projects`)
    if (resp.ok) {
      let projects = new JsonParser().parse(await resp.text()) as ProjectInfo[]
      console.log(projects)
      return projects
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getProjectDashboard(
    projectId: string,
    from?: string | null,
    to?: string | null,
    signal?: AbortSignal
  ) {
    const params = new URLSearchParams()

    from && params.append('timestamp_start', from)
    to && params.append('timestamp_end', to)

    const resp = await fetch(
      `${this.endpoint}/projects/${projectId}/dashboard?${params.toString()}`,
      { signal }
    )

    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as DashboardInfo
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getReports(projectId: string) {
    const resp = await fetch(`${this.endpoint}/projects/${projectId}/reports`)
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as ReportInfo[]
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getTestSuites(projectId: string) {
    const resp = await fetch(`${this.endpoint}/projects/${projectId}/test_suites`)
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as TestSuiteInfo[]
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getProjectInfo(projectId: string) {
    const resp = await fetch(`${this.endpoint}/projects/${projectId}/info`)
    if (resp.ok) {
      return new JsonParser().parse(await resp.text()) as ProjectDetails
    }

    throw Error(`${resp.status}, ${resp.statusText}`)
  }

  async getVersion() {
    const response = await fetch(`${this.endpoint}/version`)
    if (response.ok) {
      return (await response.json()) as VersionInfo
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async editProjectInfo(project: ProjectDetails) {
    const response = await fetch(`${this.endpoint}/projects/${project.id}/info`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(project)
    })

    if (!response.ok) {
      throw Error(`${response.status}, ${response.statusText}`)
    }

    return response
  }
}
