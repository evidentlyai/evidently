import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui/routes-components/projectId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

////////////////////
// children routes
////////////////////

import DashboardRoute from './dashboard'
import ReportsRoute from './reports'
import TestSuitesRoute from './test-suites'
import TestSuitesOldRoute from './test_suites'

export default {
  path: 'projects/:projectId',
  lazy: () => import('evidently-ui/routes-components/projectId'),
  loader,
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute, TestSuitesOldRoute]
} satisfies RouteObject
