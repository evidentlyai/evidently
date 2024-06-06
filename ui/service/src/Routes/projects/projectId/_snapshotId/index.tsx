import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { dashboardProvider } from 'api/RemoteApi'

const { loader } = getLoaderAction({ api: dashboardProvider })

export default {
  path: ':snapshotId',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshotId'
    )

    const Component = () => {
      return <SnapshotTemplate api={dashboardProvider} />
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
