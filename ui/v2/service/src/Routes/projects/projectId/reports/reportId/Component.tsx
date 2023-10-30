import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { DashboardContent } from 'evidently-ui/components/DashboardContent'
import DashboardContext, {
  CreateDashboardContextState
} from 'evidently-ui/contexts/DashboardContext'
import type { crumbFunction } from 'Components/BreadCrumbs'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { projectId, reportId } = params

  invariant(projectId, 'missing projectId')
  invariant(reportId, 'missing reportId')

  return api.getDashboard(projectId, reportId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.reportId) })
}

export const Component = () => {
  const { projectId, reportId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(reportId, 'missing reportId')

  const data = useLoaderData() as loaderData

  return (
    <>
      <DashboardContext.Provider
        value={CreateDashboardContextState({
          getAdditionGraphData: (graphId) =>
            api.getAdditionalGraphData(projectId, reportId, graphId),
          getAdditionWidgetData: (widgetId) =>
            api.getAdditionalWidgetData(projectId, reportId, widgetId)
        })}
      >
        <DashboardContent info={data} />
      </DashboardContext.Provider>
    </>
  )
}
