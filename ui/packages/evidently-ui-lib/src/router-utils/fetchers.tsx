import { useCallback, useMemo } from 'react'
import type { MatchWithAction } from '~/router-utils/types'
import { useFetcher } from '~/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from '~/utils/index'

export const useSubmitFetcherGeneral = <M extends MatchWithAction>({
  actionPath
}: {
  actionPath: ({ data }: { data: M['action']['requestData'] }) => string
}) => {
  const f = useFetcher<M['action']['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const s = useCallback(
    (data: M['action']['requestData']) =>
      f.submit(data, { action: actionPath({ data }), ...REST_PARAMS_FOR_FETCHER_SUBMIT }),
    [f]
  )

  const fetcher = useMemo(() => ({ state: f.state, data: f.data, submit: s }), [f, s])

  return fetcher
}
