import { useEffect, useState } from 'react'
import {
  type NavigateOptions,
  useFetchers,
  useLoaderData,
  useMatch,
  useMatches,
  useNavigate,
  useNavigation,
  useParams,
  useRevalidator,
  useSearchParams
} from 'react-router-dom'
import {
  type CrumbDefinition,
  type HandleWithCrumb,
  makeRouteUrl
} from '~/router-utils/router-builder'
import type { GetLinkParams, MatchAny, MatchWithLoader } from '~/router-utils/types'

export const useCurrentRouteParams = <
  K extends MatchWithLoader &
    (unknown extends K
      ? never
      : // biome-ignore lint/complexity/noBannedTypes: fine
        {})
>() => {
  const loaderData = useLoaderData() as K['loader']['returnType']
  const params = useParams() as K['params']

  const [searchParams, setSearchParams] = useSearchParams()
  const query = Object.fromEntries(searchParams) as K['loader']['query']

  /**
   * @param newQuery Pass undefined as value to remove key
   * @param navOpts
   */
  const setQuery = (newQuery: K['loader']['query'], navOpts?: NavigateOptions) => {
    setSearchParams((p) => {
      const undefinedKeys = Object.entries(newQuery)
        .filter(([_, v]) => v === undefined || !v)
        .map(([k]) => k)

      // @ts-ignore this is actually type safe
      const newQueryFiltered: Record<string, string> = Object.fromEntries(
        Object.entries(newQuery).filter(([_, v]) => v)
      )

      for (const k of undefinedKeys) {
        p.delete(k)
      }

      return {
        ...Object.fromEntries(p),
        ...newQueryFiltered
      }
    }, navOpts)
  }

  return { loaderData, params, searchParams, query, setQuery }
}

export type RouteQueryParams = Pick<
  ReturnType<typeof useCurrentRouteParams<MatchWithLoader>>,
  'query' | 'setQuery'
>

export const useOnSubmitEnd = ({
  state,
  cb
}: {
  state: 'idle' | 'loading' | 'submitting'
  cb: () => void
}) => {
  const [wasSubmit, setWasSubmit] = useState(false)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (!wasSubmit && state === 'submitting') {
      setWasSubmit(true)
    } else if (wasSubmit && state === 'idle') {
      setWasSubmit(false)
      cb()
    }
  }, [wasSubmit, state])
}

export const useIsAnyLoaderOrActionRunning = () => {
  const navigation = useNavigation()
  const fetchers = useFetchers()
  const { state } = useRevalidator()

  return (
    navigation.state !== 'idle' ||
    fetchers.some(({ state }) => state !== 'idle') ||
    state !== 'idle'
  )
}

export const useCrumbsFromHandle = () => {
  const matches = useMatches()

  const crumbs = matches
    .filter((e) => (e.handle as HandleWithCrumb)?.crumb)
    .map(({ handle, data, pathname, params }) => {
      const linkText = (() => {
        const crumb = (handle as HandleWithCrumb).crumb as CrumbDefinition

        if (crumb.title) {
          return crumb.title
        }

        if (crumb.param) {
          const c = params?.[crumb.param]
          if (c) {
            return c
          }
        }

        if (crumb.keyFromLoaderData && typeof data === 'object' && data) {
          const c = (data as Record<string, string>)?.[crumb.keyFromLoaderData]
          if (c) {
            return c
          }
        }

        return 'undefined'
      })()

      return { to: pathname, linkText }
    })

  return { crumbs }
}

export const createUseMatchRouter = <M extends MatchAny>() => {
  const hook = <K extends M['path']>({ path, end = false }: { path: K; end?: boolean }) => {
    return Boolean(useMatch({ path, end }))
  }

  return hook
}

export const createUseNavigate = <M extends MatchAny>() => {
  const hook = () => {
    const navigate = useNavigate()

    return <K extends M['path']>({
      to,
      paramsToReplace = {},
      query,
      options
    }: GetLinkParams<K, M> & { options?: NavigateOptions }) =>
      navigate(makeRouteUrl({ path: to, paramsToReplace, query }), options)
  }

  return hook
}
