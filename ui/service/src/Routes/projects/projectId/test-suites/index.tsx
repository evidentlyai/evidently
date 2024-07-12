import { Outlet, RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'

////////////////////
// children routes
////////////////////

import TestSuiteRoute from './testSuiteId'
import TestSuitesList from './testSuitesList'

import type { crumbFunction } from 'evidently-ui-lib/components/BreadCrumbs'
const crumb: crumbFunction<null> = (_, { pathname }) => ({ to: pathname, linkText: 'Test Suites' })

export default {
  id: 'test_suites',
  path: 'test-suites',
  handle: { crumb },
  Component: () => <Outlet />,
  ErrorBoundary: GenericErrorBoundary,
  children: [/* index */ TestSuitesList, TestSuiteRoute]
} satisfies RouteObject
