import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import { clientAPI } from '~/api'
import { RouterLink } from '~/routes/components'
import { useSubmitFetcher } from '~/routes/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/test-suites/?index'

type Params = GetParams<typeof currentRoutePath>
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/test_suites', { params: { path: { project_id: projectId } } })
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
    path: '/projects/:projectId/test-suites/?index',
    action: 'delete-snapshot'
  })

  const reloadSnapshotsFetcher = useSubmitFetcher({
    path: '/projects/:projectId/test-suites/?index',
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
        type='test suites'
        LinkToSnapshot={LinkToSnapshot}
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
        downloadLink={'/api/projects/{project_id}/{snapshot_id}/download'}
      />
    </>
  )
}

const LinkToSnapshot = ({ snapshotId, projectId }: { snapshotId: string; projectId: string }) => {
  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      // type safe!
      disabled={disabled}
      to={'/projects/:projectId/test-suites/:snapshotId'}
      paramsToReplace={{ projectId, snapshotId }}
      title={'View'}
    />
  )
}
