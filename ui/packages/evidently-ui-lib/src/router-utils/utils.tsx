import { redirect } from 'react-router-dom'
import { makeRouteUrl } from '~/router-utils/router-builder'
import type { GetLinkParamsByPathOnly } from '~/router-utils/types'

export const createRedirect = <Paths extends string>() => {
  const _redirect = <K extends Paths>({ to, paramsToReplace = {} }: GetLinkParamsByPathOnly<K>) =>
    redirect(makeRouteUrl({ paramsToReplace, path: to })) as never

  return _redirect
}
