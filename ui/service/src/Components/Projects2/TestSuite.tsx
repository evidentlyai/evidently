import { LoaderFunctionArgs, RouteObject, useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from '../../api/RemoteApi'
import { DashboardContent } from '../../lib/components/DashboardContent'
import DashboardContext, { CreateDashboardContextState } from '../../lib/contexts/DashboardContext'
import { satisfies } from 'semver'
import { crumbFunction } from '../BreadCrumbs'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { projectId, testSuiteId } = params

  invariant(projectId, 'missing projectId')
  invariant(testSuiteId, 'missing testSuiteId')

  return api.getDashboard(projectId, testSuiteId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname, params }) => ({ to: pathname, linkText: String(params.testSuiteId) })
}

export const Component = () => {
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

export default {
  id: 'show-test-suite-by-id',
  path: ':testSuiteId',
  loader,
  Component,
  handle
} satisfies RouteObject
