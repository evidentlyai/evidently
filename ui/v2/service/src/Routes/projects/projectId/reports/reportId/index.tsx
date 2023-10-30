import { RouteObject } from 'react-router-dom'

export default {
  id: 'show-report-by-id',
  path: ':reportId',
  lazy: () => import('./Component')
} satisfies RouteObject
