import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/test-suites/data'
import { api } from 'api/RemoteApi'

import TestSuiteRoute from './testSuiteId'

const { loader } = injectAPI({ api })

export default {
  id: 'test_suites',
  path: 'test-suites',
  lazy: () => import('evidently-ui-lib/routes-components/test-suites'),
  loader,
  children: [TestSuiteRoute]
} satisfies RouteObject
