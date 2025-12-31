///////////////////
//    ROUTE
///////////////////

import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import type { ActionArgs, GetParams } from 'evidently-ui-lib/router-utils/types'
import { clientAPI } from '~/api'
import { redirect } from '~/routes/type-safe-route-helpers/utils'

export const currentRoutePath = '/projects/:projectId/traces/:exportId'

type CurrentRouteParams = GetParams<typeof currentRoutePath>

export const actions = {
  'delete-trace': async (
    args: ActionArgs<{
      data: { traceId: string; redirectOptions: 'no-redirect' | 'redirect-to-trace' }
    }>
  ) => {
    const { data, params } = args
    const { traceId, redirectOptions } = data

    const { exportId, projectId } = params as CurrentRouteParams

    const deleteResponse = await clientAPI
      .DELETE('/api/v1/traces/{export_id}/{trace_id}', {
        params: { path: { export_id: exportId, trace_id: traceId } }
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(deleteResponse)) {
      return deleteResponse
    }

    if (redirectOptions === 'no-redirect') {
      return null
    }

    return redirect({
      to: '/projects/:projectId/traces/:exportId/trace',
      paramsToReplace: { projectId, exportId }
    })
  },
  'edit-trace-feedback': async (
    args: ActionArgs<{
      data: { traceId: string; label: string; comment: string }
    }>
  ) => {
    const { data, params } = args
    const { traceId, label, comment } = data

    const { exportId } = params as CurrentRouteParams

    const editResponse = await clientAPI
      .POST('/api/v1/traces/human_feedback', {
        params: { query: { export_id: exportId } },
        body: { trace_id: traceId, feedback: { label: label, comment: comment } }
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(editResponse)) {
      return editResponse
    }

    return null
  },
  'edit-trace-feedback-custom-shortcut-labels': async (
    args: ActionArgs<{
      data: { human_feedback_custom_shortcut_labels: string[] }
    }>
  ) => {
    const { data, params } = args
    const { human_feedback_custom_shortcut_labels } = data
    const { exportId } = params as CurrentRouteParams

    const editResponse = await clientAPI
      .PATCH('/api/datasets/{dataset_id}', {
        params: { path: { dataset_id: exportId } },
        body: {
          human_feedback_custom_shortcut_labels: human_feedback_custom_shortcut_labels
        }
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(editResponse)) {
      return editResponse
    }

    return null
  }
}
