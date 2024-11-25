import { useFetcher } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from 'evidently-ui-lib/utils/index'

import { useCallback, useMemo } from 'react'
import type { GetRouteByPath } from '~/_routes/types'
import { isPathMatchesRoutes } from '~/_routes/utils'

const routePath = '/?index'

type R = GetRouteByPath<typeof routePath>
type ActionRequestData = R['action']['args']

export const useProjectFetcher = () => {
  const f = useFetcher<R['action']['returnType']>()

  const s = useCallback(
    ({ data }: ActionRequestData) =>
      f.submit(data, {
        action: `${isPathMatchesRoutes(routePath)}`,
        ...REST_PARAMS_FOR_FETCHER_SUBMIT
      }),
    [f]
  )

  const fetcher = useMemo(() => ({ state: f.state, data: f.data, submit: s }), [f, s])

  return fetcher
}
