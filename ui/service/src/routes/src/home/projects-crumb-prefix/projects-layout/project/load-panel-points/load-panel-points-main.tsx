import { clientAPI } from 'api'
import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { BatchMetricDataModel } from 'evidently-ui-lib/api/types'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/load-panel-points'
type CurrentRouteParams = GetParams<typeof currentRoutePath>

const crumb = { title: 'Dashboard' }

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ query, params }: loadDataArgs<{ queryKeys: 'body' }>) => {
  const { projectId: project_id } = params as CurrentRouteParams

  const body = JSONParseExtended<BatchMetricDataModel>(query.body ?? '')

  if (body.series_filter && body.series_filter.length === 0) {
    return { sources: [], series: [] }
  }

  return clientAPI
    .POST('/api/v2/snapshots/{project_id}/data_series_batch', {
      params: { path: { project_id } },
      body
    })
    .then(responseParser())
}
