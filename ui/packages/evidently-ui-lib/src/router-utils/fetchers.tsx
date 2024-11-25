import { useCallback, useMemo } from 'react'
import type { Match } from '~/router-utils/types'
import { useFetcher } from '~/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from '~/utils/index'

// biome-ignore lint/suspicious/noExplicitAny: fine
export type MatchWithAction = Match<string, any, { args: { data: any }; returnType: any }>

export const useSubmitFetcherGeneral = <K extends MatchWithAction, Z extends string>({
  providePath
}: {
  providePath: ({ data }: { data: K['action']['args']['data'] }) => Extract<Z, K['path']>
}) => {
  const f = useFetcher<K['action']['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const s = useCallback(
    (data: K['action']['args']['data']) =>
      f.submit(data, { action: providePath({ data }), ...REST_PARAMS_FOR_FETCHER_SUBMIT }),
    [f]
  )

  const fetcher = useMemo(() => ({ state: f.state, data: f.data, submit: s }), [f, s])

  return fetcher
}
