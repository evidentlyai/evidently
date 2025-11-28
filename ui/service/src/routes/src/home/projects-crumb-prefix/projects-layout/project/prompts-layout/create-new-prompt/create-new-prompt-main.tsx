import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { PromptModel } from 'evidently-ui-lib/api/types'
import type { ErrorData } from 'evidently-ui-lib/api/types/utils'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { CreatePromptForm } from 'evidently-ui-lib/components/Prompts/Forms/CreatePromptForm'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { clientAPI } from '~/api'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import { redirect } from '~/routes/type-safe-route-helpers/utils'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/new'
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'New' }
export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async (_: loadDataArgs) => null

///////////////////
//    ACTIONS
///////////////////
export const actions = {
  'create-new': async ({ params, data: body }: ActionArgs<{ data: PromptModel }>) => {
    const { projectId: project_id } = params as CurrentRouteParams

    const response = await clientAPI
      .POST('/api/prompts', { params: { query: { project_id } }, body })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(response)) {
      return response
    }

    if (!response.id) {
      return { error: { detail: 'Missing prompt id', status_code: false } } satisfies ErrorData
    }

    return redirect({
      to: '/projects/:projectId/prompts/:promptId',
      paramsToReplace: { projectId: project_id, promptId: response.id }
    })
  }
}

///////////////////
//  COMPONENT
///////////////////
export const Component = () => {
  const {
    params: { projectId }
  } = useCurrentRouteParams<CurrentRoute>()

  const createPromptFetcher = useSubmitFetcher({
    path: '/projects/:projectId/prompts/new',
    action: 'create-new'
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <Box my={2}>
      <CreatePromptForm
        isLoading={isLoading}
        defaultValues={{ name: '' }}
        onSubmit={(data) => createPromptFetcher.submit({ data, paramsToReplace: { projectId } })}
      />
    </Box>
  )
}
