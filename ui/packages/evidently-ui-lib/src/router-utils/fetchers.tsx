import { useCallback, useMemo } from 'react'
import type { GetParams, MatchAny, MatchWithAction } from '~/router-utils/types'
import { useFetcher } from '~/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from '~/utils/index'
import { replaceParamsInLink } from './utils'

export const useSubmitFetcherGeneral = <M extends MatchWithAction, K extends keyof M['action']>({
  action,
  path,
  provideParams
}: {
  action: K
  path: M['path']
  provideParams: ({ data }: { data: M['action'][K]['requestData'] }) => GetParams<M['path']>
}) => {
  const originalFetcher = useFetcher<M['action'][K]['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const submit = useCallback(
    (data: M['action'][K]['requestData']) => {
      const params = provideParams({ data })

      originalFetcher.submit(
        // @ts-ignore
        { data, action },
        {
          action: replaceParamsInLink(params, path),
          ...REST_PARAMS_FOR_FETCHER_SUBMIT
        }
      )
    },
    [originalFetcher, path]
  )

  const fetcher = useMemo(
    () => ({ state: originalFetcher.state, data: originalFetcher.data, submit: submit }),
    [originalFetcher, submit]
  )

  return fetcher
}

// Helper function to infer K
export const createUseSubmitFetcherGeneral = <M extends MatchAny>() => {
  type MatchesWithAction = Extract<M, MatchWithAction>

  const hook = <
    Path extends MatchesWithAction['path'],
    ActionName extends keyof Extract<MatchesWithAction, { path: Path }>['action']
  >(args: {
    action: ActionName
    path: Path
    provideParams: ({
      data
    }: {
      data: Extract<MatchesWithAction, { path: Path }>['action'][ActionName]['requestData']
    }) => GetParams<Extract<MatchesWithAction, { path: Path }>['path']>
  }) => useSubmitFetcherGeneral<Extract<MatchesWithAction, { path: Path }>, ActionName>(args)

  return hook
}
