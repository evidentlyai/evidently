import React from 'react'

import type { AdditionalGraphInfo, WidgetInfo } from '~/api'

class CachedDashboardContextState implements DashboardContextState {
  cachedGraphs: Map<string, AdditionalGraphInfo>
  cachedWidgets: Map<string, WidgetInfo>
  inner: DashboardContextState

  constructor(inner: DashboardContextState) {
    this.inner = inner
    this.cachedGraphs = new Map<string, AdditionalGraphInfo>()
    this.cachedWidgets = new Map<string, WidgetInfo>()
  }

  async getAdditionGraphData(graphId: string): Promise<AdditionalGraphInfo> {
    let cached = this.cachedGraphs.get(graphId)
    if (cached !== undefined) {
      return cached
    }
    cached = await this.inner.getAdditionGraphData(graphId)
    this.cachedGraphs.set(graphId, cached)
    return cached
  }

  async getAdditionWidgetData(widgetId: string): Promise<WidgetInfo> {
    let cached = this.cachedWidgets.get(widgetId)
    if (cached !== undefined) {
      return cached
    }
    cached = await this.inner.getAdditionWidgetData(widgetId)
    this.cachedWidgets.set(widgetId, cached)
    return cached
  }
}

export interface DashboardContextState {
  getAdditionGraphData: (graphId: string) => Promise<AdditionalGraphInfo>
  getAdditionWidgetData: (widgetId: string) => Promise<WidgetInfo>
}

const DashboardContext = React.createContext<DashboardContextState>({
  getAdditionGraphData: () =>
    new Promise((_, reject) => reject("default context doesn't contain methods to get data")),
  getAdditionWidgetData: () =>
    new Promise((_, reject) => reject("default context doesn't contain methods to get data"))
})

export function CreateDashboardContextState(
  state: DashboardContextState
): CachedDashboardContextState {
  return new CachedDashboardContextState(state)
}

export default DashboardContext
