import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContentWidgets } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import { crumbFunction } from '~/components/BreadCrumbs'
import { LoaderData } from './data'
import { Grid } from '@mui/material'
import { DashboardProvider } from '~/api/types/providers/dashboard'
import { AdditionalGraphInfo, WidgetInfo } from '~/api'

export const handle: { crumb: crumbFunction<LoaderData> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.snapshotId) })
}

export const SnapshotTemplate = ({ api }: { api: DashboardProvider }) => {
  const { projectId, snapshotId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(snapshotId, 'missing snapshotId')

  const data = useLoaderData() as LoaderData
  return (
    <>
      <DashboardContext.Provider
        value={CreateDashboardContextState({
          getAdditionGraphData: (graphId) =>
            api.getDashboardGraph({
              project: { id: projectId },
              snapshot: { id: snapshotId },
              graph: { id: graphId }
            }) as Promise<AdditionalGraphInfo>,
          getAdditionWidgetData: (widgetId) =>
            api.getDashboardGraph({
              project: { id: projectId },
              snapshot: { id: snapshotId },
              graph: { id: widgetId }
            }) as Promise<WidgetInfo>
        })}
      >
        <Grid container spacing={3} direction="row" alignItems="stretch">
          <DashboardContentWidgets widgets={data.widgets} />
        </Grid>
      </DashboardContext.Provider>
    </>
  )
}
