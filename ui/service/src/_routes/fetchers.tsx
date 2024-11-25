import { useFetcher } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from 'evidently-ui-lib/utils/index'
import { useCallback, useMemo } from 'react'
import type { Match, PathsWithDynamicSegments } from '~/_routes/types'

export const useSubmitFetcher = <
  // biome-ignore lint/suspicious/noExplicitAny: fine
  K extends Match<string, any, { args: { data: any }; returnType: any }>
>({
  providePath
}: {
  providePath: ({
    data
  }: { data: K['action']['args']['data'] }) => Extract<PathsWithDynamicSegments, K['path']>
}) => {
  const f = useFetcher<K['action']['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const s = useCallback(
    (data: K['action']['args']['data']) =>
      f.submit(data, { action: providePath(data), ...REST_PARAMS_FOR_FETCHER_SUBMIT }),
    [f]
  )

  const fetcher = useMemo(() => ({ state: f.state, data: f.data, submit: s }), [f, s])

  return fetcher
}
