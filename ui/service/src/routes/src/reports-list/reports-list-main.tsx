import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import { RouterLink } from '~/routes/components'
import { useSubmitFetcher } from '~/routes/hooks'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/reports/?index'

type Params = GetParams<typeof currentRoutePath>

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/snapshots', { params: { path: { project_id: projectId } } })
    .then(responseParser())
}

export const actions = {
  'reload-snapshots': ({ params }: ActionArgs) => {
    const { projectId } = params as Params

    return clientAPI
      .GET('/api/projects/{project_id}/reload', {
        params: { path: { project_id: projectId } }
      })
      .then(responseParser({ notThrowExc: true }))
  },
  'delete-snapshot': ({ params, data }: ActionArgs<{ data: { snapshotId: string } }>) => {
    const { projectId } = params as Params

    return clientAPI
      .DELETE('/api/projects/{project_id}/{snapshot_id}', {
        params: { path: { project_id: projectId, snapshot_id: data.snapshotId } }
      })
      .then(responseParser({ notThrowExc: true }))
  }
}

export const Component = () => {
  const { loaderData: reports, params, query } = useCurrentRouteParams<CurrentRoute>()

  const { projectId } = params

  const deleteSnapshotFetcher = useSubmitFetcher({
    path: '/projects/:projectId/reports/?index',
    action: 'delete-snapshot'
  })

  const reloadSnapshotsFetcher = useSubmitFetcher({
    path: '/projects/:projectId/reports/?index',
    action: 'reload-snapshots'
  })

  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <>
      <SnapshotsListTemplate
        query={query}
        disabled={disabled}
        projectId={params.projectId}
        snapshots={reports}
        LinkToSnapshot={LinkToSnapshot}
        downloadLink={'/api/projects/{project_id}/{snapshot_id}/download'}
        onDeleteSnapshot={({ snapshotId }) => {
          if (confirm('Are you sure?') === true) {
            deleteSnapshotFetcher.submit({
              data: { snapshotId },
              paramsToReplace: { projectId }
            })
          }
        }}
        onReloadSnapshots={() =>
          reloadSnapshotsFetcher.submit({ data: {}, paramsToReplace: { projectId } })
        }
      />
    </>
  )
}

const LinkToSnapshot = ({ snapshotId, projectId }: { snapshotId: string; projectId: string }) => {
  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      disabled={disabled}
      // type safe!
      to={'/projects/:projectId/reports/:snapshotId'}
      paramsToReplace={{ projectId, snapshotId }}
      title={'View'}
    />
  )
}
