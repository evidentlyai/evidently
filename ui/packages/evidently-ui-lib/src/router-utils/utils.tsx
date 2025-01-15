import { redirect } from 'react-router-dom'
import { makeRouteUrl } from '~/router-utils/router-builder'
import type { GetLinkParams, MatchAny } from '~/router-utils/types'

export const CreateRedirect = <M extends MatchAny>() => {
  const redirectResult = <K extends M['path']>({
    to,
    query,
    paramsToReplace = {}
  }: GetLinkParams<K, M>) => {
    const toActual = makeRouteUrl({ paramsToReplace, query, path: to })

    return redirect(toActual)
  }

  return redirectResult
}
