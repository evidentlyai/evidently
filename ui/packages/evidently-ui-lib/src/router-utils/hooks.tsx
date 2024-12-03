import { useEffect, useState } from 'react'
import {
  useFetchers,
  useLoaderData,
  useMatches,
  useNavigation,
  useParams,
  useRevalidator,
  useSearchParams
} from 'react-router-dom'
import type { MatchWithLoader } from '~/router-utils/types'
import type { HandleWithCrumb } from '~/router-utils/utils'

export const useRouteParams = <
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

  return { loaderData, params, query, setSearchParams }
}

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
    .map(({ handle, data, pathname, params }) => ({
      to: `${pathname}`,
      linkText:
        (handle as HandleWithCrumb)?.crumb?.title ??
        params[(handle as HandleWithCrumb)?.crumb?.param ?? ''] ??
        (typeof data === 'object'
          ? (data as Record<string, string>)[
              (handle as HandleWithCrumb)?.crumb?.keyFromLoaderData ?? ''
            ]
          : '') ??
        `undefined (provide title or param in crumb). Path: ${pathname}`
    }))

  return { crumbs }
}
