import type { GetRouteByPath } from '~/routes/types'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { SnapshotTemplateComponent } from 'evidently-ui-lib/routes-components/snapshotId'
import { getSnapshotInfo } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

export const _route_path = (!0 as boolean)
  ? '/:projectId/reports/:snapshotId'
  : '/:projectId/test-suites/:snapshotId'

type Path = typeof _route_path

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { param: 'snapshotId' satisfies keyof Params }

export const handle = { crumb }

export const loaderSpecial = ({ params }: LoaderSpecialArgs) => {
  const { projectId, snapshotId } = params as Params

  return getSnapshotInfo({ api: clientAPI, projectId, snapshotId })
}

export const Component = () => {
  const { loaderData, params } = useRouteParams<CurrentRoute>()

  const { projectId, snapshotId } = params

  return (
    <SnapshotTemplateComponent
      api={clientAPI}
      projectId={projectId}
      snapshotId={snapshotId}
      data={loaderData}
    />
  )
}
