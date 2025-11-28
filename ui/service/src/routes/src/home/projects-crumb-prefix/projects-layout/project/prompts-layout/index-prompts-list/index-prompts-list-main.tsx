import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Add as AddIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'
import invariant from 'tiny-invariant'
import { PromptsTable } from '~/Components/Prompts/PromptsTable'
import { clientAPI } from '~/api'
import { useProjectInfo } from '~/contexts/project'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/?index'
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { projectId: project_id } = params as CurrentRouteParams

  return clientAPI
    .GET('/api/prompts', { params: { query: { project_id } } })
    .then(responseParser())
    .then((prompts) => ({ prompts }))
}

///////////////////
//  COMPONENT
///////////////////
export const Component = () => {
  const {
    loaderData: { prompts },
    params: { projectId }
  } = useCurrentRouteParams<CurrentRoute>()

  const deletePromptFetcher = useSubmitFetcher({
    path: '/projects/:projectId/prompts/:promptId',
    action: 'delete-prompt'
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <PromptsTable
      prompts={prompts}
      isLoading={isLoading}
      onDelete={(promptId) => {
        if (confirm('Are you sure?') === true) {
          deletePromptFetcher.submit({
            data: { redirectOptions: 'no-redirect' },
            paramsToReplace: { projectId, promptId }
          })
        }
      }}
      GetPromptLinkByID={GetPromptLinkByID}
      createNewPromptButton={
        <RouterLink
          type='button'
          size='medium'
          variant='outlined'
          startIcon={<AddIcon />}
          to='/projects/:projectId/prompts/new'
          paramsToReplace={{ projectId }}
          title={'Create new prompt'}
        />
      }
      createFirstPromptButton={
        <RouterLink
          type='button'
          size='large'
          variant='contained'
          startIcon={<AddIcon />}
          to='/projects/:projectId/prompts/new'
          paramsToReplace={{ projectId }}
          title={'Create your first prompt'}
        />
      }
    />
  )
}

const GetPromptLinkByID = ({ promptId }: { promptId: string }) => {
  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project
  const isLoaing = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      disabled={isLoaing}
      title={'View'}
      to={'/projects/:projectId/prompts/:promptId'}
      paramsToReplace={{ projectId, promptId }}
    />
  )
}
