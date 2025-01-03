import type { GetRouteByPath } from '~/routes/types'

import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { SnapshotTemplateComponent } from 'evidently-ui-lib/routes-components/snapshotId'
import { getSnapshotInfo } from 'evidently-ui-lib/routes-components/snapshotId/data'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = (!0 as boolean)
  ? '/projects/:projectId/reports/:snapshotId'
  : '/projects/:projectId/test-suites/:snapshotId'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { param: 'snapshotId' satisfies keyof Params }

export const handle = { crumb }

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId, snapshotId } = params as Params

  return getSnapshotInfo({ api: clientAPI, projectId, snapshotId })
}

export const Component = () => {
  const { loaderData, params } = useCurrentRouteParams<CurrentRoute>()

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
