import { clientAPI } from 'api'
import type { BatchMetricDataModel } from 'api/types'
import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/v2/projects/:projectId/api/load-panel-points'
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    LOADER
///////////////////
export const loadData = ({ query, params }: loadDataArgs<{ queryKeys: 'body' }>) => {
  const { projectId: project_id } = params as CurrentRouteParams

  const body = JSONParseExtended<BatchMetricDataModel>(query.body)

  return clientAPI
    .POST('/api/v2/snapshots/{project_id}/data_series_batch', {
      params: { path: { project_id } },
      body
    })
    .then(responseParser())
}
