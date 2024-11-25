import { useFetcher } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from 'evidently-ui-lib/utils/index'

import { useCallback } from 'react'
import { type GetRouteByPath, isPathMatchesRoutes } from '~/_routes/types'

type R = GetRouteByPath<'/?index'>

export const useProjectFetcher = () => {
  const fetcher = useFetcher<R['action']['returnType']>()

  const submit = useCallback(
    ({ data }: R['action']['args']) =>
      fetcher.submit(data, {
        action: `${isPathMatchesRoutes('/?index')}`,
        ...REST_PARAMS_FOR_FETCHER_SUBMIT
      }),
    [fetcher]
  )

  const { state, data } = fetcher

  return { state, data, submit }
}
