import { RouteObject } from 'react-router-dom'

import TestSuiteRoute from './testSuiteId'

export default {
  id: 'test_suites',
  path: 'test-suites',
  lazy: () => import('./Component'),
  children: [TestSuiteRoute]
} satisfies RouteObject
