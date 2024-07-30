import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContentWidgets } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import { crumbFunction } from '~/components/BreadCrumbs'
import { LoaderData } from './data'
import { Grid } from '@mui/material'
import { AdditionalGraphInfo, WidgetInfo } from '~/api'
import { API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import { JSONParseExtended } from '~/api/JsonParser'

export const handle: { crumb: crumbFunction<LoaderData>; hide: Record<string, Boolean> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.snapshotId) }),
  hide: {
    snapshotList: true
  }
}

export const SnapshotTemplate = ({ api }: { api: API_CLIENT_TYPE }) => {
  const { projectId, snapshotId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(snapshotId, 'missing snapshotId')

  const data = useLoaderData() as LoaderData
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
        <Grid container spacing={3} direction="row" alignItems="stretch">
          <DashboardContentWidgets widgets={data.widgets} />
        </Grid>
      </DashboardContext.Provider>
    </>
  )
}
