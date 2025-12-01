import type { Expect, TYPE_SATISFIED } from 'evidently-ui-lib/api/types/utils'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { createRedirect } from 'evidently-ui-lib/router-utils/utils'
import type { Paths } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/prompts/:promptId/?index'
type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { promptId, projectId } = params as CurrentRouteParams

  return redirect({
    to: '/projects/:projectId/prompts/:promptId/manage',
    paramsToReplace: { promptId, projectId }
  })
}

const redirect = (() => {
  const paths = ['/projects/:projectId/prompts/:promptId/manage'] as const
  type RedirectPaths = (typeof paths)[number]

  // @ts-ignore
  type TYPE_GUARD =
    // path is real
    Expect<TYPE_SATISFIED<RedirectPaths, Paths>>

  return createRedirect<RedirectPaths>()
})()
