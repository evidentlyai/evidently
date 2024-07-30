import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { clientAPI } from '~/api'

const { loader } = getLoaderAction({ api: clientAPI })

export default {
  path: ':snapshotId',
  lazy: async () => {
    const { SnapshotTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/snapshotId'
    )

    const Component = () => {
      return <SnapshotTemplate api={clientAPI} />
    }

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
