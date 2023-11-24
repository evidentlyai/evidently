import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContent } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'
import { Api } from '~/api'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.snapshotId) })
}

export const SnapshotTemplate = ({ api }: { api: Api }) => {
  const { projectId, snapshotId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(snapshotId, 'missing snapshotId')

  const data = useLoaderData() as loaderData
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
        <DashboardContent widgets={data.widgets} />
      </DashboardContext.Provider>
    </>
  )
}
