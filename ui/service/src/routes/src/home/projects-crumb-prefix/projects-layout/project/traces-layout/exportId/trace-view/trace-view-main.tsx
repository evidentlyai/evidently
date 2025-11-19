import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { TraceViewer } from 'evidently-ui-lib/components/Traces/TraceViewer/index'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { clientAPI } from '~/api'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces/:exportId/trace'

type CurrentRouteParams = GetParams<typeof currentRoutePath>
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
///////////////////
//    CRUMB
///////////////////

const crumb: CrumbDefinition = {
  keyFromLoaderData: 'name' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////

export const loadData = async ({ params }: loadDataArgs<{ queryKeys: 'trace-id' }>) => {
  const { exportId } = params as CurrentRouteParams

  return clientAPI
    .GET('/api/v1/traces/list', {
      params: { query: { export_id: exportId, getter_type: 'ungrouped' } }
    })
    .then(responseParser())
    .then((traces) => ({ traces: traces.sessions, name: traces.metadata.name }))
}

///////////////////
//  COMPONENT
///////////////////

export const Component = () => {
  const { loaderData: data, params, query } = useCurrentRouteParams<CurrentRoute>()

  const defaultTraceId = query['trace-id']

  const { projectId, exportId } = params

  const isLoading = useIsAnyLoaderOrActionRunning()

  const deleteTrace = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId',
    action: 'delete-trace'
  })

  return (
    <TraceViewer
      key={exportId}
      defaultTraceId={defaultTraceId}
      data={Object.values(data.traces).flat()}
      isLoading={isLoading}
      onDelete={(traceId) => {
        if (confirm('Are you sure?') === true) {
          deleteTrace.submit({
            data: { traceId, redirectOptions: 'no-redirect' },
            paramsToReplace: { projectId, exportId }
          })
        }
      }}
    />
  )
}
