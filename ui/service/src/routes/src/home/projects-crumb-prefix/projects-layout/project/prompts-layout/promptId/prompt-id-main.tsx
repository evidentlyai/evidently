import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/:promptId'
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = {
  keyFromLoaderData: 'promptName' satisfies keyof CurrentRoute['loader']['returnType']
}
export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { promptId: prompt_id } = params as CurrentRouteParams

  return clientAPI
    .GET('/api/prompts/{prompt_id}', { params: { path: { prompt_id } } })
    .then(responseParser())
    .then(({ name: promptName }) => ({ promptName }))
}

///////////////////
//    ACTIONS
///////////////////
export const actions = {
  'delete-prompt': async ({ params }: ActionArgs<{ data: { redirectOptions: 'no-redirect' } }>) => {
    const { promptId: prompt_id } = params as CurrentRouteParams

    return clientAPI
      .DELETE('/api/prompts/{prompt_id}', { params: { path: { prompt_id } } })
      .then(responseParser({ notThrowExc: true }))
  }
}
