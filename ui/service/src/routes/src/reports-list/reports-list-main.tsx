import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { createUseSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import { useIsAnyLoaderOrActionRunning, useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import { getReports, getSnapshotsActions } from 'evidently-ui-lib/routes-components/snapshots/data'
import { RouterLink } from '~/routes/components'

///////////////////
//    ROUTE
///////////////////

export const _route_path = '/:projectId/reports/?index'
type Path = typeof _route_path

type Params = GetParams<Path>

type CurrentRoute = GetRouteByPath<Path>

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId } = params as Params

  return getReports({ api: clientAPI, projectId })
}

export const actions = getSnapshotsActions({ api: clientAPI })

const useFetcher = createUseSubmitFetcherGeneral<CurrentRoute>()

export const Component = () => {
  const { loaderData: reports, params } = useRouteParams<CurrentRoute>()

  const { projectId } = params

  const deleteSnapshotFetcher = useFetcher({
    actionPath: () => ({ path: '/:projectId/reports/?index', params: { projectId } }),
    action: 'delete-snapshot'
  })

  const reloadSnapshotsFetcher = useFetcher({
    actionPath: () => ({ path: '/:projectId/reports/?index', params: { projectId } }),
    action: 'reload-snapshots'
  })

  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <>
      <SnapshotsListTemplate
        disabled={disabled}
        projectId={params.projectId}
        snapshots={reports}
        type='reports'
        LinkToSnapshot={LinkToSnapshot}
        onDeleteSnapshot={({ snapshotId }) =>
          deleteSnapshotFetcher.submit({ snapshotId, projectId })
        }
        onReloadSnapshots={() => reloadSnapshotsFetcher.submit({ projectId })}
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
      to={'/:projectId/reports/:snapshotId'}
      paramsToReplace={{ projectId, snapshotId }}
      title={'View'}
    />
  )
}
