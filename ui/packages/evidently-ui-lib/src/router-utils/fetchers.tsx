import { useCallback, useMemo } from 'react'
import type { GetParams, MatchWithAction } from '~/router-utils/types'
import { useFetcher } from '~/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from '~/utils/index'
import { replaceParamsInLink } from './utils'

export const useSubmitFetcherGeneral = <M extends MatchWithAction, K extends keyof M['action']>({
  actionPath,
  action
}: {
  action: K
  actionPath: ({ data }: { data: M['action'][K]['requestData'] }) => {
    path: M['path']
    params: GetParams<M['path']>
  }
}) => {
  const originalFetcher = useFetcher<M['action'][K]['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const submit = useCallback(
    (data: M['action'][K]['requestData']) => {
      const { params, path } = actionPath({ data })

      originalFetcher.submit(
        // @ts-ignore
        { data, action },
        {
          action: replaceParamsInLink(params, path),
          ...REST_PARAMS_FOR_FETCHER_SUBMIT
        }
      )
    },
    [originalFetcher]
  )

  const fetcher = useMemo(
    () => ({ state: originalFetcher.state, data: originalFetcher.data, submit: submit }),
    [originalFetcher, submit]
  )

  return fetcher
}

// Helper function to infer K
export const createUseSubmitFetcherGeneral = <M extends MatchWithAction>() => {
  const hook = <K extends keyof M['action']>(args: {
    action: K
    actionPath: ({ data }: { data: M['action'][K]['requestData'] }) => {
      path: M['path']
      params: GetParams<M['path']>
    }
  }) => useSubmitFetcherGeneral<M, K>(args)

  return hook
}
