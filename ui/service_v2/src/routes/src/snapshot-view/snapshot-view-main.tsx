import type { AdditionalGraphInfo, WidgetInfo } from 'evidently-ui-lib/api'
import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { DashboardInfoModel } from 'evidently-ui-lib/api/types'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { SnapshotTemplateComponent } from 'evidently-ui-lib/routes-components/snapshotId'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/reports/:snapshotId'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { param: 'snapshotId' satisfies keyof Params }

export const handle = { crumb }

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId, snapshotId } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/{snapshot_id}/data', {
      params: { path: { project_id: projectId, snapshot_id: snapshotId } },
      parseAs: 'text'
    })
    .then(responseParser())
    .then(JSONParseExtended<DashboardInfoModel>)
}

export const Component = () => {
  const { loaderData: data, params } = useCurrentRouteParams<CurrentRoute>()

  const { projectId, snapshotId } = params

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
