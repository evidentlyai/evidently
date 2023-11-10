import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  id: 'show-report-by-id',
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
  loader
} satisfies RouteObject
