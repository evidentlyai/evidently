import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import { getReports, getSnapshotsActions } from 'evidently-ui-lib/routes-components/snapshots/data'
import { RouterLink } from '~/routes/components'
import { useSubmitFetcher } from '~/routes/hooks'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/:projectId/reports/?index'

type Params = GetParams<typeof currentRoutePath>

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId } = params as Params

  return getReports({ api: clientAPI, projectId })
}

export const actions = getSnapshotsActions({ api: clientAPI })

// type OOO = GetRouteByPath<'/:projectId/reports/:snapshotId'>['']
export const Component = () => {
  const { loaderData: reports, params } = useCurrentRouteParams<CurrentRoute>()

  const { projectId } = params

  const deleteSnapshotFetcher = useSubmitFetcher({
    path: '/:projectId/reports/?index',
    action: 'delete-snapshot',
    provideParams: ({ data: { projectId } }) => ({ projectId })
  })

  const reloadSnapshotsFetcher = useSubmitFetcher({
    path: '/:projectId/reports/?index',
    action: 'reload-snapshots',
    provideParams: ({ data: { projectId } }) => ({ projectId })
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
