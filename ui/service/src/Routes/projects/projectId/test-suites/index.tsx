import { injectTestSuitesAPI } from 'evidently-ui-lib/routes-components/snapshots/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'

import { ActionsErrorSnackbar, GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import TestSuiteRoute from './testSuiteId'

const { loader, action } = injectTestSuitesAPI({ api: clientAPI })

export default {
  id: 'test_suites',
  path: 'test-suites',
  lazy: async () => {
    const { SnapshotsListTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshots'
    )

    const Component = () => (
      <>
        <ActionsErrorSnackbar />
        <SnapshotsListTemplate type='test suites' />
      </>
    )

    return { ...rest, Component }
  },
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary,
  children: [TestSuiteRoute]
} satisfies RouteObject
