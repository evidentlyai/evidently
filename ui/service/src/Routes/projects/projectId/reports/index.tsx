import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectReportsAPI } from 'evidently-ui-lib/routes-components/snapshots/data'
import { api } from 'api/RemoteApi'

const { loader, action } = injectReportsAPI({ api })

////////////////////
// children routes
////////////////////

import ReportRoute from './reportId'

export default {
  id: 'reports',
  path: 'reports',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshots'
    )

    const Component = () => <SnapshotTemplate type="report" />

    return { ...rest, Component }
  },
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary,
  children: [ReportRoute]
} satisfies RouteObject
