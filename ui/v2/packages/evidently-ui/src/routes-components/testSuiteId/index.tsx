import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardContent } from '~/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '~/contexts/DashboardContext'
import { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'
import { Api } from '~/api'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname, params }) => ({ to: pathname, linkText: String(params.testSuiteId) })
}

export const TestSuiteTemplate = ({ api }: { api: Api }) => {
  const { projectId, testSuiteId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(testSuiteId, 'missing testSuiteId')

  const data = useLoaderData() as loaderData
  return (
    <>
      <DashboardContext.Provider
        value={CreateDashboardContextState({
          getAdditionGraphData: (graphId) =>
            api.getAdditionalGraphData(projectId, testSuiteId, graphId),
          getAdditionWidgetData: (widgetId) =>
            api.getAdditionalWidgetData(projectId, testSuiteId, widgetId)
        })}
      >
        <DashboardContent info={data} />
      </DashboardContext.Provider>
    </>
  )
}
