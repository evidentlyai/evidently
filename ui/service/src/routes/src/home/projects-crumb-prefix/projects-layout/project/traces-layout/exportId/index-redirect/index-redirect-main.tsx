import type { Expect, TYPE_SATISFIED } from 'evidently-ui-lib/api/types/utils'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { createRedirect } from 'evidently-ui-lib/router-utils/utils'
import type { Paths } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces/:exportId/?index'

type CurrentRouteParams = GetParams<typeof currentRoutePath>

///////////////////
//    LOADER
///////////////////

export const loadData = async ({ params }: loadDataArgs) => {
  const { exportId, projectId } = params as CurrentRouteParams

  return redirect({
    to: '/projects/:projectId/traces/:exportId/trace',
    paramsToReplace: { exportId, projectId }
  })
}

const redirect = (() => {
  const paths = [
    '/projects/:projectId/traces/:exportId/dialog',
    '/projects/:projectId/traces/:exportId/trace',
    '/projects/:projectId/traces/:exportId/dataset'
  ] as const
  type RedirectPaths = (typeof paths)[number]

  // @ts-ignore
  type TYPE_GUARD =
    // path is real
    Expect<TYPE_SATISFIED<RedirectPaths, Paths>>

  return createRedirect<RedirectPaths>()
})()
