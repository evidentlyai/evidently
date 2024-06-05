import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import LoadableView from '~/components/LoadableVIew'
import ApiContext from '~/contexts/ApiContext'
import { DashboardWidgets } from '~/components/DashboardWidgets'

export function ProjectReport(props: { projectId: string; reportId: string }) {
  const { projectId, reportId } = props
  return (
    <>
      <ApiContext.Consumer>
        {({ Api }) => (
          <DashboardContext.Provider
            value={CreateDashboardContextState({
              getAdditionGraphData: (graphId) =>
                Api.getAdditionalGraphData(projectId, reportId, graphId),
              getAdditionWidgetData: (widgetId) =>
                Api.getAdditionalWidgetData(projectId, reportId, widgetId)
            })}
          >
            <LoadableView func={() => Api.getDashboard(projectId, reportId)}>
              {(params) => <DashboardWidgets widgets={params.widgets} />}
            </LoadableView>
          </DashboardContext.Provider>
        )}
      </ApiContext.Consumer>
    </>
  )
}
