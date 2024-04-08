import {
  Api,
  AdditionalGraphInfo,
  DashboardInfo,
  ProjectDetails,
  ProjectInfo,
  SnapshotInfo,
  VersionInfo,
  WidgetInfo
} from './index'

import { JsonParser } from './JsonParser'

export async function fetchThrow(...args: Parameters<typeof fetch>) {
  const response = await fetch(...args)

  if (!response.ok && response.status >= 400) {
    // smth went wrong
    throw response
  }

  return response
}

export class RemoteApi implements Api {
  private readonly endpoint: string

  public constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  async getAdditionalGraphData(
    projectId: string,
    dashboardId: string,
    graphId: string
  ): Promise<AdditionalGraphInfo> {
    const response = await fetchThrow(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${graphId}`
    )

    return new JsonParser().parse(await response.text())
  }

  async getAdditionalWidgetData(
    projectId: string,
    dashboardId: string,
    widgetId: string
  ): Promise<WidgetInfo> {
    const response = await fetchThrow(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${widgetId}`
    )

    return new JsonParser().parse(await response.text())
  }

  async getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
    const response = await fetchThrow(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`)

    return new JsonParser().parse(await response.text())
  }

  async getProjects(): Promise<ProjectInfo[]> {
    const response = await fetchThrow(`${this.endpoint}/projects`)

    return new JsonParser().parse(await response.text())
  }

  async getProjectDashboard(
    projectId: string,
    from?: string | null,
    to?: string | null
  ): Promise<DashboardInfo> {
    const params = new URLSearchParams()

    from && params.append('timestamp_start', from)
    to && params.append('timestamp_end', to)

    const response = await fetchThrow(
      `${this.endpoint}/projects/${projectId}/dashboard?${params.toString()}`
    )

    return new JsonParser().parse(await response.text())
  }

  async getReports(projectId: string): Promise<SnapshotInfo[]> {
    const response = await fetchThrow(`${this.endpoint}/projects/${projectId}/reports`)

    return new JsonParser().parse(await response.text())
  }

  async getTestSuites(projectId: string): Promise<SnapshotInfo[]> {
    const response = await fetchThrow(`${this.endpoint}/projects/${projectId}/test_suites`)

    return new JsonParser().parse(await response.text())
  }

  async getProjectInfo(projectId: string): Promise<ProjectDetails> {
    const response = await fetchThrow(`${this.endpoint}/projects/${projectId}/info`)

    return new JsonParser().parse(await response.text())
  }

  async getVersion(): Promise<VersionInfo> {
    const response = await fetchThrow(`${this.endpoint}/version`)

    return response.json()
  }

  async editProjectInfo(project: ProjectDetails) {
    return fetchThrow(`${this.endpoint}/projects/${project.id}/info`, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(project)
    })
  }

  async reloadProject(projectId: string) {
    return fetchThrow(`${this.endpoint}/projects/${projectId}/reload`)
  }

  async createProject(project: Partial<ProjectDetails>): Promise<ProjectDetails> {
    const params = new URLSearchParams()
    project.team_id && params.append('team_id', project.team_id)

    const response = await fetchThrow(`${this.endpoint}/projects?${params.toString()}`, {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project)
    })

    return response.json()
  }

  async deleteProject(projectId: string): Promise<Response> {
    return fetchThrow(`${this.endpoint}/projects/${projectId}`, {
      method: 'delete'
    })
  }
}
