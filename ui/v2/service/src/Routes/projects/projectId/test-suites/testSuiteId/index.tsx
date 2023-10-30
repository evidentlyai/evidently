import { RouteObject } from 'react-router-dom'

export default {
  id: 'show-test-suite-by-id',
  path: ':testSuiteId',
  lazy: () => import('./Component')
} satisfies RouteObject
