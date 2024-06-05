import { Api, AdditionalGraphInfo, WidgetInfo } from './index'

import { JsonParser } from '~/api/JsonParser'
import { DashboardInfoModel } from '~/api/types'

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

  async getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfoModel> {
    const response = await fetchThrow(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`)

    return new JsonParser().parse(await response.text())
  }
}
