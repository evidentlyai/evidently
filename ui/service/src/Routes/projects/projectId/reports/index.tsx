import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { Outlet, RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

////////////////////
// children routes
////////////////////

import ReportRoute from './reportId'
import ReportsListRoute from './reportsList'

import type { crumbFunction } from 'evidently-ui-lib/components/BreadCrumbs'
const crumb: crumbFunction<null> = (_, { pathname }) => ({ to: pathname, linkText: 'Reports' })

export default {
  id: 'reports',
  path: 'reports',
  handle: { crumb },
  Component: () => <Outlet />,
  ErrorBoundary: GenericErrorBoundary,
  children: [/* index */ ReportsListRoute, ReportRoute]
} satisfies RouteObject
