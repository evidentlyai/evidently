import { Grid } from '@mui/material'
import type { AdditionalGraphInfo, WidgetInfo } from '~/api'
import { JSONParseExtended } from '~/api/JsonParser'
import { type API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import type { DashboardInfoModel } from '~/api/types'
import { DashboardContentWidgets } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'

export const SnapshotTemplateComponent = ({
  api,
  data,
  projectId,
  snapshotId
}: { api: API_CLIENT_TYPE; data: DashboardInfoModel; projectId: string; snapshotId: string }) => {
  return (
    <>
      <DashboardContext.Provider
        value={CreateDashboardContextState({
          getAdditionGraphData: (graphId) =>
            api
              .GET('/api/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}', {
                params: {
                  path: {
                    project_id: projectId,
                    snapshot_id: snapshotId,
                    graph_id: encodeURIComponent(graphId)
                  }
                },
                parseAs: 'text'
              })
              .then(responseParser())
              .then(JSONParseExtended<AdditionalGraphInfo>),
          getAdditionWidgetData: (widgetId) =>
            api
              .GET('/api/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}', {
                params: {
                  path: {
                    project_id: projectId,
                    snapshot_id: snapshotId,
                    graph_id: encodeURIComponent(widgetId)
                  }
                },
                parseAs: 'text'
              })
              .then(responseParser())
              .then(JSONParseExtended<WidgetInfo>)
        })}
      >
        <Grid container spacing={3} direction='row' alignItems='stretch'>
          <DashboardContentWidgets widgets={data.widgets} />
        </Grid>
      </DashboardContext.Provider>
    </>
  )
}
