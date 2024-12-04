import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { GetRouteByPath } from '~/_routes/types'

import { clientAPI } from '~/api'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { SnapshotsListTemplate } from 'evidently-ui-lib/routes-components/snapshots'
import { getSnapshots } from 'evidently-ui-lib/routes-components/snapshots/data'
import { RouterLink } from '~/_routes/components'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId/reports'

type Params = GetParams<Path>

type CurrentRoute = GetRouteByPath<Path>

const crumb: CrumbDefinition = { title: 'Reports' }
export const handle = { crumb }

export const loaderSpecial = ({ params }: LoaderSpecialArgs) => {
  const { projectId } = params as Params

  return getSnapshots({ api: clientAPI, snapshotType: 'reports', projectId })
}

export const Component = () => {
  const { loaderData: reports, params } = useRouteParams<CurrentRoute>()

  const { projectId } = params

  return (
    <>
      <SnapshotsListTemplate
        projectId={params.projectId}
        snapshots={reports}
        type='reports'
        LinkToSnapshot={() => (
          <RouterLink
            type='button'
            // type safe!
            to={'/:projectId/reports'}
            paramsToReplace={{ projectId }}
            title={'View'}
          />
        )}
      />
    </>
  )
}
