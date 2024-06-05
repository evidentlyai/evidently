import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/projectId/data'
import { projectProvider } from 'api/RemoteApi'

const { loader } = injectAPI({ api: projectProvider })

////////////////////
// children routes
////////////////////

import DashboardRoute from './dashboard'
import ReportsRoute from './reports'
import TestSuitesRoute from './test-suites'

export default {
  path: 'projects/:projectId',
  lazy: () => import('evidently-ui-lib/routes-components/projectId'),
  loader,
  ErrorBoundary: GenericErrorBoundary,
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute]
} satisfies RouteObject
