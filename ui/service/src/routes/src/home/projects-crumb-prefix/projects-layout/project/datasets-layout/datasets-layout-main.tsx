import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { Schemas } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams } from 'evidently-ui-lib/router-utils/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import { redirect } from '~/routes/type-safe-route-helpers/utils'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/datasets'

type CurrentRouteParams = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Datasets' }

export const handle = { crumb }

export const actions = {
  'export-to-dataset-from-source-and-redirect-to-dataset': async (
    args: ActionArgs<{ data: Schemas['MaterializeDatasetRequest'] }>
  ) => {
    const { data, params } = args
    const { projectId } = params as CurrentRouteParams

    const response = await clientAPI
      .POST('/api/datasets/materialize', {
        params: { query: { project_id: projectId } },
        body: data
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(response)) {
      return response
    }

    return redirect({
      to: '/projects/:projectId/datasets/:datasetId',
      paramsToReplace: { projectId, datasetId: response.dataset_id }
    })
  }
}

export const Component = () => (
  <Box mt={2}>
    <Outlet />
  </Box>
)
