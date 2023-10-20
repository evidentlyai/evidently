import { RouteObject } from 'react-router-dom'

////////////////////
// children routes
////////////////////

import DashboardRoute from './dashboard'
import ReportsRoute from './reports'
import TestSuitesRoute from './test-suites'
import TestSuitesOldRoute from './test_suites'

export default {
  path: 'projects/:projectId',
  lazy: () => import('./Component'),
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute, TestSuitesOldRoute]
} satisfies RouteObject
