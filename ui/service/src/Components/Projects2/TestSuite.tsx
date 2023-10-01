import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from '../../api/RemoteApi'
import { DashboardContent } from '../../lib/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '../../lib/contexts/DashboardContext'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { projectId, testSuiteId } = params

  invariant(projectId, 'missing projectId')
  invariant(testSuiteId, 'missing testSuiteId')

  return api.getDashboard(projectId, testSuiteId)
}

export const TestSuite = () => {
  const { projectId, testSuiteId } = useParams()
  invariant(projectId, 'missing projectId')
  invariant(testSuiteId, 'missing testSuiteId')

  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>
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
