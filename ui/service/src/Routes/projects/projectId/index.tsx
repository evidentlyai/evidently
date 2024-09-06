import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/projectId/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'

const { loader } = getLoaderAction({ api: clientAPI })

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
