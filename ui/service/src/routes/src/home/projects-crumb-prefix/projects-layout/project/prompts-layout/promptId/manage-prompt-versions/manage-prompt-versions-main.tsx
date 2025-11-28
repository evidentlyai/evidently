import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import type { ModeType } from 'evidently-ui-lib/components/Prompts/ToggleViewEdit'
import { editState2PromptVersion } from 'evidently-ui-lib/components/Prompts/Versions/utils'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning,
  useOnSubmitEnd
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Add as AddIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import { useState } from 'react'
import { ManagePromptVersions } from '~/Components/Prompts/ManagePromptVersions'
import { clientAPI } from '~/api'
import { PromptViewer } from '~/flows/prompts/PromptViewer'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/:promptId/manage'
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'Manage Versions' }
export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { promptId: prompt_id } = params as CurrentRouteParams

  const [prompts, promptVersions, latestPromptVersion] = await Promise.all([
    clientAPI
      .GET('/api/llm_judges/templates')
      .then(responseParser())
      .then((template) =>
        template.map(({ prompt, ...rest }) => ({
          ...rest,
          prompt: prompt.replaceAll('{input}', '{{input}}').trim()
        }))
      ),
    clientAPI
      .GET('/api/prompts/{prompt_id}/versions', {
        params: { path: { prompt_id } }
      })
      .then(responseParser()),
    clientAPI
      .GET('/api/prompts/{prompt_id}/versions/{version}', {
        params: { path: { prompt_id, version: 'latest' } }
      })
      .then(responseParser({ notThrowExc: true }))
      .then((data) => (isSuccessData(data) ? data : null))
  ])

  return { prompts, promptVersions, latestPromptVersion }
}

///////////////////
//    ACTIONS
///////////////////
export const actions = {
  'delete-prompt-version': async (
    args: ActionArgs<{ data: { redirectOptions: 'no-redirect'; prompt_version_id: string } }>
  ) => {
    const { data } = args

    return clientAPI
      .DELETE('/api/prompts/prompt-versions/{prompt_version_id}', {
        params: { path: { prompt_version_id: data.prompt_version_id } }
      })
      .then(responseParser({ notThrowExc: true }))
  }
}

///////////////////
//  COMPONENT
///////////////////
export const Component = () => {
  const {
    loaderData,
    params: { promptId, projectId }
  } = useCurrentRouteParams<CurrentRoute>()

  const { promptVersions, latestPromptVersion, prompts } = loaderData

  const [mode, onModeChange] = useState<ModeType>('view')

  const [selectedPromptVersionId, onChangeSelectedPromptVersionId] = useState(
    latestPromptVersion?.id ?? null
  )

  const createPromptVersionFetcher = useSubmitFetcher({
    path: '/projects/:projectId/prompts/:promptId/new-version',
    action: 'create-new'
  })

  useOnSubmitEnd({
    state: createPromptVersionFetcher.state,
    cb: () => {
      if (!isSuccessData(createPromptVersionFetcher.data)) {
        return
      }

      onModeChange('view')
      onChangeSelectedPromptVersionId(latestPromptVersion?.id ?? '')
    }
  })

  const deletePromptVersionFetcher = useSubmitFetcher({
    path: '/projects/:projectId/prompts/:promptId/manage',
    action: 'delete-prompt-version'
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  //////////////////////
  // STATE GUARDS
  //////////////////////

  // 1. Reset selectedPromptVersionId if it doesn't exist in promptVersions
  // in case of deleting prompt version
  if (selectedPromptVersionId && !promptVersions.find((p) => p.id === selectedPromptVersionId)) {
    onChangeSelectedPromptVersionId(latestPromptVersion?.id ?? null)
  }

  return (
    <ManagePromptVersions
      promptId={promptId}
      promptVersions={promptVersions}
      latestPromptVersion={latestPromptVersion}
      selectedPromptVersionId={selectedPromptVersionId}
      onChangeSelectedPromptVersionId={onChangeSelectedPromptVersionId}
      mode={mode}
      onModeChange={onModeChange}
      createNewVersionButton={
        <RouterLink
          type='button'
          startIcon={<AddIcon />}
          title='Create new version'
          to={'/projects/:projectId/prompts/:promptId/new-version'}
          variant='outlined'
          size={'small'}
          paramsToReplace={{ promptId, projectId }}
        />
      }
      createFirstVersionButton={
        <RouterLink
          type='button'
          size='medium'
          startIcon={<AddIcon />}
          title={"Create prompt's first version"}
          to={'/projects/:projectId/prompts/:promptId/new-version'}
          variant='contained'
          disabled={isLoading}
          paramsToReplace={{ promptId, projectId }}
        />
      }
      editPromptVersionProps={{
        prompts,
        PromptViewerComponent: PromptViewer,
        saveAsNewVersionDisabled: createPromptVersionFetcher.state !== 'idle',
        onSaveAsNewVersion: (editState) => {
          createPromptVersionFetcher.submit({
            data: {
              body: editState2PromptVersion({ editState }),
              redirectTo: 'no-redirect'
            },
            paramsToReplace: { projectId, promptId }
          })
        }
      }}
      viewPromptVersionProps={{
        PromptViewerComponent: PromptViewer,
        isDeleteDisabled: deletePromptVersionFetcher.state !== 'idle',
        onDeletePromptVersion: (promptVersionId) => {
          if (confirm('Are you sure?') === true) {
            deletePromptVersionFetcher.submit({
              data: { redirectOptions: 'no-redirect', prompt_version_id: promptVersionId },
              paramsToReplace: { projectId, promptId }
            })
          }
        }
      }}
    />
  )
}
