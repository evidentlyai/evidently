import { Box } from '@mui/material'
import type { AdditionalGraphInfo, WidgetInfo } from '~/api'
import { JSONParseExtended } from '~/api/JsonParser'
import { type API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import type { DashboardInfoModel } from '~/api/types'
import { SnapshotWidgets } from '~/components/WidgetsContent'
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
        <Box py={2}>
          <SnapshotWidgets widgets={data.widgets} />
        </Box>
      </DashboardContext.Provider>
    </>
  )
}
