import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  path: ':snapshotId',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshotId'
    )

    const Component = () => {
      return <SnapshotTemplate api={api} />
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
