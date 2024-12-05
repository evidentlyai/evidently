import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { useIsAnyLoaderOrActionRunning, useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import {
  getReports,
  getSnapshotsActionSpecial
} from 'evidently-ui-lib/routes-components/snapshots/data'
import { RouterLink } from '~/routes/components'
import { useSubmitFetcher } from '~/routes/fetchers'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId/reports/?index'

type Params = GetParams<Path>

type CurrentRoute = GetRouteByPath<Path>

export const loaderSpecial = ({ params }: LoaderSpecialArgs) => {
  const { projectId } = params as Params

  return getReports({ api: clientAPI, projectId })
}

export const actionSpecial = getSnapshotsActionSpecial({ api: clientAPI })

export const Component = () => {
  const { loaderData: reports, params } = useRouteParams<CurrentRoute>()

  const { projectId } = params

  const fetcher = useSubmitFetcher<CurrentRoute>({
    actionPath: () => ({ path: '/:projectId/reports/?index', params: { projectId } })
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
          fetcher.submit({
            action: 'delete-snapshot',
            snapshotId,
            projectId
          })
        }
        onReloadSnapshots={() =>
          fetcher.submit({
            action: 'reload-snapshots',
            projectId
          })
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
      to={'/:projectId/reports/:snapshotId'}
      paramsToReplace={{ projectId, snapshotId }}
      title={'View'}
    />
  )
}
