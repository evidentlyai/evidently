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
  const f = useFetcher<M['action'][K]['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const s = useCallback(
    (data: M['action'][K]['requestData']) =>
      f.submit(
        // @ts-ignore
        { data, action },
        {
          action: replaceParamsInLink(actionPath({ data }).params, actionPath({ data }).path),
          ...REST_PARAMS_FOR_FETCHER_SUBMIT
        }
      ),
    [f]
  )

  const fetcher = useMemo(() => ({ state: f.state, data: f.data, submit: s }), [f, s])

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
