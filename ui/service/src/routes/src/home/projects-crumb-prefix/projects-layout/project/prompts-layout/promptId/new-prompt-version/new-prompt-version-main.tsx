import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { LLMPromptTemplateModel, PromptVersionModel } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { PromptVersionForm } from 'evidently-ui-lib/components/Prompts/Versions/Edit/index'
import { CreateFirstPromptVersionForm } from 'evidently-ui-lib/components/Prompts/Versions/Forms/CreateFirstPromptVersionForm'
import {
  editState2PromptVersion,
  promptVersion2EditState
} from 'evidently-ui-lib/components/Prompts/Versions/utils'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { clientAPI } from '~/api'
import { PromptViewer } from '~/flows/prompts/PromptViewer'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import { redirect } from '~/routes/type-safe-route-helpers/utils'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/:promptId/new-version'
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'New Version' }
export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { promptId: prompt_id } = params as CurrentRouteParams

  return Promise.all([
    [] as LLMPromptTemplateModel[], // TODO: Add prompts templates later
    clientAPI
      .GET('/api/prompts/{prompt_id}/versions/{version}', {
        params: { path: { prompt_id, version: 'latest' } }
      })
      .then(responseParser({ notThrowExc: true }))
      .then((data) => (isSuccessData(data) ? data : null))
  ]).then(([prompts, latestPromptVersion]) => ({ prompts, latestPromptVersion }))
}

///////////////////
//    ACTIONS
///////////////////
export const actions = {
  'create-new': async (
    args: ActionArgs<{
      data: {
        body: Omit<PromptVersionModel, 'version'>
        redirectTo: 'manage' | 'no-redirect'
      }
    }>
  ) => {
    const { params, data } = args
    const { body, redirectTo } = data

    const { promptId: prompt_id } = params as CurrentRouteParams

    const latestVersionResponse = await clientAPI
      .GET('/api/prompts/{prompt_id}/versions/{version}', {
        params: { path: { prompt_id, version: 'latest' } }
      })
      .then(responseParser({ notThrowExc: true }))
      .then((data) => (isSuccessData(data) ? data : null))

    const latestVersion = latestVersionResponse ? latestVersionResponse.version : 0
    const newVersion = latestVersion + 1

    const response = await clientAPI
      .POST('/api/prompts/{prompt_id}/versions', {
        params: { path: { prompt_id } },
        body: { ...body, version: newVersion }
      })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(response)) {
      return response
    }

    if (redirectTo === 'no-redirect') {
      return null
    }

    const { projectId, promptId } = params as CurrentRouteParams

    return redirect({
      to: `/projects/:projectId/prompts/:promptId/${redirectTo}`,
      paramsToReplace: { projectId, promptId }
    })
  }
}

///////////////////
//  COMPONENT
///////////////////
export const Component = () => {
  const { loaderData, params } = useCurrentRouteParams<CurrentRoute>()

  const { latestPromptVersion: promptVersion, prompts } = loaderData
  const { projectId, promptId } = params

  const createPromptFetcher = useSubmitFetcher({
    path: '/projects/:projectId/prompts/:promptId/new-version',
    action: 'create-new'
  })

  const defaultValues = promptVersion2EditState({ promptVersion })
  const isFirstVersion = !promptVersion

  if (isFirstVersion) {
    return (
      <Box maxWidth={'md'} mx={'auto'} mt={3}>
        <CreateFirstPromptVersionForm
          PromptViewerComponent={PromptViewer}
          onSuccess={(editState) => {
            createPromptFetcher.submit({
              data: {
                body: editState2PromptVersion({ editState }),
                redirectTo: 'manage'
              },
              paramsToReplace: { projectId, promptId }
            })
          }}
          defaultValues={defaultValues}
          prompts={prompts}
        />
      </Box>
    )
  }

  return (
    <Box maxWidth={'md'} mx={'auto'} mt={3}>
      <PromptVersionForm
        PromptViewerComponent={PromptViewer}
        prompts={prompts}
        onSuccess={(editState) => {
          createPromptFetcher.submit({
            data: {
              body: editState2PromptVersion({ editState }),
              redirectTo: 'manage'
            },
            paramsToReplace: { projectId, promptId }
          })
        }}
        defaultValues={defaultValues}
        buttonTitle='Save'
      />
    </Box>
  )
}
