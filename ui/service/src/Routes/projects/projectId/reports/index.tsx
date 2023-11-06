import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/reports/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

////////////////////
// children routes
////////////////////

import ReportRoute from './reportId'

export default {
  id: 'reports',
  path: 'reports',
  lazy: () => import('evidently-ui-lib/routes-components/reports'),
  loader,
  children: [ReportRoute]
} satisfies RouteObject
