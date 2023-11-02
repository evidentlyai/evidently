import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContent } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import type { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'
import type { Api } from '~/api'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.reportId) })
}

export const ReportTemplate = ({ api }: { api: Api }) => {
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
