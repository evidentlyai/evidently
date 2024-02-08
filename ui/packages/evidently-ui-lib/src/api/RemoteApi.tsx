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

import { JsonParser } from './JsonParser'

const throwIfStatus = (status: number) => (response: Response) => {
  if (!response.ok && response.status === status) {
    throw response
  }
}

const throwIfStatus401 = throwIfStatus(401)

export class RemoteApi implements Api {
  private readonly endpoint: string

  public constructor(endpoint: string) {
    this.endpoint = endpoint
  }

  async getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string) {
    const response = await fetch(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${graphId}`
    )

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as AdditionalGraphInfo
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getAdditionalWidgetData(
    projectId: string,
    dashboardId: string,
    widgetId: string
  ): Promise<WidgetInfo> {
    const response = await fetch(
      `${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${widgetId}`
    )

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as WidgetInfo
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getDashboard(projectId: string, dashboardId: string) {
    const response = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`)

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as DashboardInfo
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getProjects() {
    const response = await fetch(`${this.endpoint}/projects`)

    throwIfStatus401(response)

    if (response.ok) {
      let projects = new JsonParser().parse(await response.text()) as ProjectInfo[]
      console.log(projects)
      return projects
    }

    throw Error(`${response.status}, ${response.statusText}`)
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

    const response = await fetch(
      `${this.endpoint}/projects/${projectId}/dashboard?${params.toString()}`,
      { signal }
    )

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as DashboardInfo
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getReports(projectId: string) {
    const response = await fetch(`${this.endpoint}/projects/${projectId}/reports`)

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as SnapshotInfo[]
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getTestSuites(projectId: string) {
    const response = await fetch(`${this.endpoint}/projects/${projectId}/test_suites`)

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as SnapshotInfo[]
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getProjectInfo(projectId: string) {
    const response = await fetch(`${this.endpoint}/projects/${projectId}/info`)

    throwIfStatus401(response)

    if (response.ok) {
      return new JsonParser().parse(await response.text()) as ProjectDetails
    }

    throw Error(`${response.status}, ${response.statusText}`)
  }

  async getVersion() {
    const response = await fetch(`${this.endpoint}/version`)

    throwIfStatus401(response)

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

    throwIfStatus401(response)

    if (!response.ok) {
      throw Error(`${response.status}, ${response.statusText}`)
    }

    return response
  }

  async reloadProject(projectId: string) {
    const response = await fetch(`${this.endpoint}/projects/${projectId}/reload`)

    throwIfStatus401(response)

    if (!response.ok) {
      throw response
    }

    return response
  }

  async createProject(project: Partial<ProjectDetails>): Promise<ProjectDetails> {
    const params = new URLSearchParams()
    project.team_id && params.append('team_id', project.team_id)

    const response = await fetch(`${this.endpoint}/projects?${params.toString()}`, {
      method: 'post',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project)
    })

    throwIfStatus401(response)

    if (!response.ok) {
      throw Error(`${response.status}, ${response.statusText}`)
    }

    return response.json()
  }

  async deleteProject(projectId: string): Promise<Response> {
    const response = await fetch(`${this.endpoint}/projects/${projectId}`, {
      method: 'delete'
    })

    if (response.ok) {
      return response
    }

    throw Error(`${response.status}, ${response.statusText}, ${await response.text()}`)
  }
}
