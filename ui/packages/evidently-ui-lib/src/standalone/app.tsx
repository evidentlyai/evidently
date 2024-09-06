import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'

import type { AdditionalGraphInfo, WidgetInfo } from '~/api'
import type { DashboardInfoModel } from '~/api/types'
import { DashboardWidgets } from '~/components/DashboardWidgets'

export function StandaloneSnapshotWidgets({
  dashboard: { widgets },
  additionalGraphs
}: {
  dashboard: DashboardInfoModel
  additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>
}) {
  return (
    <DashboardContext.Provider
      value={CreateDashboardContextState({
        getAdditionGraphData: (graphId) => {
          const data = additionalGraphs.get(graphId)
          if (data) {
            return Promise.resolve(data as AdditionalGraphInfo)
          }

          return Promise.reject('No graph found')
        },
        getAdditionWidgetData: (widgetId) => {
          const data = additionalGraphs.get(widgetId)
          if (data) {
            return Promise.resolve(data as WidgetInfo)
          }

          return Promise.reject('No graph found')
        }
      })}
    >
      <DashboardWidgets widgets={widgets} />
    </DashboardContext.Provider>
  )
}
