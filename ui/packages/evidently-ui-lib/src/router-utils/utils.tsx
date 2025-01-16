import { redirect } from 'react-router-dom'
import { makeRouteUrl } from '~/router-utils/router-builder'
import type { GetLinkParamsByPath } from '~/router-utils/types'

export const redirectTypeSafe = <K extends string>({
  to,
  paramsToReplace = {}
}: GetLinkParamsByPath<K>) => {
  const toActual = makeRouteUrl({ paramsToReplace, path: to })

  return redirect(toActual)
}
