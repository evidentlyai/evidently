import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'

import { DashboardWidgets } from '~/components/DashboardWidgets'
import { DashboardInfoModel } from '~/api/types'
import { AdditionalGraphInfo, WidgetInfo } from '~/api'

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
