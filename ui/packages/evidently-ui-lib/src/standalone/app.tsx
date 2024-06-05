import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import LoadableView from '~/components/LoadableVIew'
import ApiContext from '~/contexts/ApiContext'
import { DashboardWidgets } from '~/components/DashboardWidgets'

export function ProjectSnapshot(props: { projectId: string; snapshotId: string }) {
  const { projectId, snapshotId } = props
  return (
    <>
      <ApiContext.Consumer>
        {({ Api }) => (
          <DashboardContext.Provider
            value={CreateDashboardContextState({
              getAdditionGraphData: (graphId) =>
                Api.getAdditionalGraphData(projectId, snapshotId, graphId),
              getAdditionWidgetData: (widgetId) =>
                Api.getAdditionalWidgetData(projectId, snapshotId, widgetId)
            })}
          >
            <LoadableView func={() => Api.getDashboard(projectId, snapshotId)}>
              {(params) => <DashboardWidgets widgets={params.widgets} />}
            </LoadableView>
          </DashboardContext.Provider>
        )}
      </ApiContext.Consumer>
    </>
  )
}
