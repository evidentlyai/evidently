import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { createUseSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import { useIsAnyLoaderOrActionRunning, useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import {
  getSnapshotsActionSpecial,
  getTestSuites
} from 'evidently-ui-lib/routes-components/snapshots/data'
import { RouterLink } from '~/routes/components'

///////////////////
//    ROUTE
///////////////////

export const _route_path = '/:projectId/test-suites/?index'
type Path = typeof _route_path

type Params = GetParams<Path>

type CurrentRoute = GetRouteByPath<Path>

export const loaderSpecial = ({ params }: LoaderSpecialArgs) => {
  const { projectId } = params as Params

  return getTestSuites({ api: clientAPI, projectId })
}

export const actions = getSnapshotsActionSpecial({ api: clientAPI })

const useFetcher = createUseSubmitFetcherGeneral<CurrentRoute>()

export const Component = () => {
  const { loaderData: reports, params } = useRouteParams<CurrentRoute>()

  const { projectId } = params

  const deleteSnapshotFetcher = useFetcher({
    action: 'delete-snapshot',
    actionPath: () => ({ path: '/:projectId/test-suites/?index', params: { projectId } })
  })

  const reloadSnapshotsFetcher = useFetcher({
    action: 'reload-snapshots',
    actionPath: () => ({ path: '/:projectId/test-suites/?index', params: { projectId } })
  })

  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <>
      <SnapshotsListTemplate
        disabled={disabled}
        projectId={params.projectId}
        snapshots={reports}
        type='test suites'
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
      // type safe!
      disabled={disabled}
      to={'/:projectId/test-suites/:snapshotId'}
      paramsToReplace={{ projectId, snapshotId }}
      title={'View'}
    />
  )
}
