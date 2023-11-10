import { RouteObject } from 'react-router-dom'
import { injectTestSuitesAPI } from 'evidently-ui-lib/routes-components/snapshots/data'
import { api } from 'api/RemoteApi'

import TestSuiteRoute from './testSuiteId'

const { loader } = injectTestSuitesAPI({ api })

export default {
  id: 'test_suites',
  path: 'test-suites',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshots'
    )

    const Component = () => <SnapshotTemplate type="test-suite" />

    return { ...rest, Component }
  },
  loader,
  children: [TestSuiteRoute]
} satisfies RouteObject
