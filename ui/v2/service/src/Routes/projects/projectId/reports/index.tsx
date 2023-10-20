import { RouteObject } from 'react-router-dom'

////////////////////
// children routes
////////////////////

import ReportRoute from './reportId'

export default {
  id: 'reports',
  path: 'reports',
  lazy: () => import('./Component'),
  children: [ReportRoute]
} satisfies RouteObject
