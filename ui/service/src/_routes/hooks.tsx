import {
  useFetchers,
  useLoaderData,
  useNavigation,
  useParams,
  useRevalidator
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useEffect, useState } from 'react'

export const useRouteParams = <
  // biome-ignore lint/suspicious/noExplicitAny: fine
  K extends { params: Record<string, string>; loader: { returnType: any } } & (unknown extends K
    ? never
    : // biome-ignore lint/complexity/noBannedTypes: fine
      {})
>() => {
  const loaderData = useLoaderData() as K['loader']['returnType']
  const params = useParams() as K['params']

  return { loaderData, params }
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
