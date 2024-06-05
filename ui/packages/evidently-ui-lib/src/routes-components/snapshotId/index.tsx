import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContentWidgets } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import { crumbFunction } from '~/components/BreadCrumbs'
import { LoaderData } from './data'
import { DashboardAPI } from '~/api'
import { Grid } from '@mui/material'

export const handle: { crumb: crumbFunction<LoaderData>; hide: Record<string, Boolean> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.snapshotId) }),
  hide: {
    snapshotList: true
  }
}

export const SnapshotTemplate = ({ api }: { api: DashboardAPI }) => {
  const { projectId, snapshotId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(snapshotId, 'missing snapshotId')

  const data = useLoaderData() as LoaderData
  return (
    <>
      <DashboardContext.Provider
        value={CreateDashboardContextState({
          getAdditionGraphData: (graphId) =>
            api.getAdditionalGraphData(projectId, snapshotId, graphId),
          getAdditionWidgetData: (widgetId) =>
            api.getAdditionalWidgetData(projectId, snapshotId, widgetId)
        })}
      >
        <Grid container spacing={3} direction="row" alignItems="stretch">
          <DashboardContentWidgets widgets={data.widgets} />
        </Grid>
      </DashboardContext.Provider>
    </>
  )
}
