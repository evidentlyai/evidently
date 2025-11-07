import type { AdditionalGraphInfo, WidgetInfo } from 'evidently-ui-lib/api'
import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { DashboardInfoModel } from 'evidently-ui-lib/api/types'
import { SnapshotTemplateComponent } from 'evidently-ui-lib/routes-components/snapshotId'
import { clientAPI } from '~/api'

type SnapshotViewProps = {
  data: DashboardInfoModel
  projectId: string
  snapshotId: string
}

export const SnapshotView = ({ data, projectId, snapshotId }: SnapshotViewProps) => {
  return (
    <SnapshotTemplateComponent
      data={data}
      dashboardContextState={{
        getAdditionGraphData: (graphId) =>
          clientAPI
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
          clientAPI
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
      }}
    />
  )
}
