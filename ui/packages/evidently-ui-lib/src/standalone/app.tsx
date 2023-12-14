import { Api, DashboardInfo } from '~/api'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import LoadableView from '~/components/LoadableVIew'
import ApiContext from '~/contexts/ApiContext'
import { DashboardWidgets } from '~/components/DashboardWidgets'

export function Report(props: { params: DashboardInfo }) {
  return <DashboardWidgets widgets={props.params.widgets} />
}

export const ProjectDashboard = (props: { projectId: string; from?: string; to?: string }) => {
  const callback = (api: Api) => api.getProjectDashboard(props.projectId, props.from, props.to)
  return (
    <>
      <ApiContext.Consumer>
        {(api) => (
          <LoadableView func={() => callback(api.Api)}>
            {(params) => (
              <>
                <Report params={params} />
              </>
            )}
          </LoadableView>
        )}
      </ApiContext.Consumer>
    </>
  )
}

export function ProjectReport(props: { projectId: string; reportId: string }) {
  const { projectId, reportId } = props
  return (
    <>
      <ApiContext.Consumer>
        {(api) => (
          <DashboardContext.Provider
            value={CreateDashboardContextState({
              getAdditionGraphData: (graphId) =>
                api.Api!.getAdditionalGraphData(projectId, reportId, graphId),
              getAdditionWidgetData: (widgetId) =>
                api.Api!.getAdditionalWidgetData(projectId, reportId, widgetId)
            })}
          >
            <LoadableView func={() => api.Api.getDashboard(projectId, reportId)}>
              {(params) => <Report params={params} />}
            </LoadableView>
          </DashboardContext.Provider>
        )}
      </ApiContext.Consumer>
    </>
  )
}
