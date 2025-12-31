import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { FeedbackForm } from 'evidently-ui-lib/components/HumanFeedback/FeedbackForm'
import { TraceViewer } from 'evidently-ui-lib/components/Traces/TraceViewer/index'
import { extractFeedbackData } from 'evidently-ui-lib/components/Traces/TraceViewer/utils'
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

  const metadataPromise = clientAPI
    .GET('/api/datasets/{dataset_id}/metadata', {
      params: { path: { dataset_id: exportId } }
    })
    .then(responseParser())

  const dataPromise = clientAPI
    .GET('/api/v1/traces/list', {
      params: { query: { export_id: exportId, getter_type: 'ungrouped' } }
    })
    .then(responseParser())

  const [metadata, data] = await Promise.all([metadataPromise, dataPromise])

  return {
    traces: data.sessions,
    name: data.metadata.name,
    human_feedback_custom_shortcut_labels: metadata.human_feedback_custom_shortcut_labels
  }
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

  const editTraceFeedbackFetcher = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId',
    action: 'edit-trace-feedback'
  })

  const editTraceFeedbackCustomShortcutLabelsFetcher = useSubmitFetcher({
    path: '/projects/:projectId/traces/:exportId',
    action: 'edit-trace-feedback-custom-shortcut-labels'
  })

  const additionalLabels = data.human_feedback_custom_shortcut_labels ?? []

  return (
    <TraceViewer
      key={exportId}
      traceComponent={({ trace }) => (
        <FeedbackForm
          key={trace.trace_id}
          buttonText='Save'
          evaluationZero
          defaultFeedbackData={extractFeedbackData(trace)}
          onSubmitFeedbackData={(data) => {
            editTraceFeedbackFetcher.submit({
              data: { traceId: trace.trace_id, label: data.label, comment: data.comment },
              paramsToReplace: { projectId, exportId }
            })
          }}
          submitDisabled={editTraceFeedbackFetcher.state !== 'idle'}
          additionalLabels={additionalLabels}
          setAdditionalLabels={(human_feedback_custom_shortcut_labels) => {
            editTraceFeedbackCustomShortcutLabelsFetcher.submit({
              data: { human_feedback_custom_shortcut_labels },
              paramsToReplace: { projectId, exportId }
            })
          }}
          additionalLabelsDisabled={editTraceFeedbackCustomShortcutLabelsFetcher.state !== 'idle'}
        />
      )}
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
