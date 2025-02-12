import { useCallback, useMemo } from 'react'
import { makeRouteUrl } from '~/router-utils/router-builder'
import type {
  GetParamsOptional,
  MatchAny,
  MatchWithAction,
  MatchWithLoader
} from '~/router-utils/types'
import {
  type SubmitOptions,
  useActionData,
  useFetcher,
  useNavigation,
  useSubmit
} from '~/shared-dependencies/react-router-dom'
import { REST_PARAMS_FOR_FETCHER_SUBMIT } from '~/utils/index'

export const useSubmitFetcherGeneral = <M extends MatchWithAction, K extends keyof M['action']>({
  action,
  path
}: {
  action: K
  path: M['path']
}) => {
  const originalFetcher = useFetcher<M['action'][K]['returnType']>()

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const submit = useCallback(
    ({
      data,
      paramsToReplace = {}
    }: { data: M['action'][K]['requestData'] } & GetParamsOptional<M['path']>) => {
      originalFetcher.submit(
        // @ts-ignore
        { data, action },
        {
          action: makeRouteUrl({ paramsToReplace, path }),
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

export const createUseSubmitFetcherGeneral = <M extends MatchAny>() => {
  type MatchesWithAction = Extract<M, MatchWithAction>

  const hook = <
    Path extends MatchesWithAction['path'],
    ActionName extends keyof Extract<MatchesWithAction, { path: Path }>['action']
  >(args: {
    action: ActionName
    path: Path
  }) => useSubmitFetcherGeneral<Extract<MatchesWithAction, { path: Path }>, ActionName>(args)

  return hook
}

export const useSubmitGeneral = <M extends MatchWithAction, K extends keyof M['action']>({
  action,
  path
}: {
  action: K
  path: M['path']
}) => {
  const originalSumit = useSubmit()
  const navigattion = useNavigation()
  const data = useActionData() as M['action'][K]['returnType'] | undefined

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const submit = useCallback(
    ({
      data,
      paramsToReplace = {},
      submitOptions
    }: { data: M['action'][K]['requestData']; submitOptions?: SubmitOptions } & GetParamsOptional<
      M['path']
    >) => {
      originalSumit(
        // @ts-ignore
        { data, action },
        {
          action: makeRouteUrl({ paramsToReplace, path }),
          ...submitOptions,
          ...REST_PARAMS_FOR_FETCHER_SUBMIT
        }
      )
    },
    [originalSumit, path]
  )

  return { state: navigattion.state, submit, data }
}

export const createUseSubmitGeneral = <M extends MatchAny>() => {
  type MatchesWithAction = Extract<M, MatchWithAction>

  const hook = <
    Path extends MatchesWithAction['path'],
    ActionName extends keyof Extract<MatchesWithAction, { path: Path }>['action']
  >(args: {
    action: ActionName
    path: Path
  }) => useSubmitGeneral<Extract<MatchesWithAction, { path: Path }>, ActionName>(args)

  return hook
}

export const useLoaderGeneral = <M extends MatchWithLoader>(path: M['path']) => {
  const originalFetcher = useFetcher<M['loader']['returnType']>()

  const load = useCallback(
    ({
      query,
      paramsToReplace = {}
    }: { query?: M['loader']['query'] } & GetParamsOptional<M['path']>) =>
      originalFetcher.load(makeRouteUrl({ paramsToReplace, path, query: query })),
    [originalFetcher, path]
  )

  const fetcher = useMemo(
    () => ({ state: originalFetcher.state, data: originalFetcher.data, load }),
    [originalFetcher, load]
  )

  return fetcher
}

export const createUseLoaderGeneral = <M extends MatchAny>() => {
  type MatchesWithLoader = Extract<M, MatchWithLoader>

  const hook = <Path extends MatchesWithLoader['path']>(path: Path) =>
    useLoaderGeneral<Extract<MatchesWithLoader, { path: Path }>>(path)

  return hook
}
