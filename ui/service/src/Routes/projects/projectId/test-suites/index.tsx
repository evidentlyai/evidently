import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectTestSuitesAPI } from 'evidently-ui-lib/routes-components/snapshots/data'
import { api } from 'api/RemoteApi'

import TestSuiteRoute from './testSuiteId'
import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'

const { loader, action } = injectTestSuitesAPI({ api })

export default {
  id: 'test_suites',
  path: 'test-suites',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshots'
    )

    const Component = () => <SnapshotTemplate type="test suite" />

    return { ...rest, Component }
  },
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary,
  children: [TestSuiteRoute]
} satisfies RouteObject
