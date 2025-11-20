import React, { useEffect, useState } from 'react'
export * from '@uidotdev/usehooks'

// biome-ignore lint/suspicious/noExplicitAny: <explanation>
export const useStableCallbackWithLatestScope = <T extends (...args: any[]) => any>(
  callback: T
) => {
  const callbackRef = React.useRef(callback)

  React.useLayoutEffect(() => {
    callbackRef.current = callback
  }, [callback])

  return React.useCallback((...args: Parameters<T>) => callbackRef.current(...args), []) as T
}

export const useTimeout = (timeout?: number) => {
  const [isOver, setIsOver] = useState<boolean>(false)

  const delay = timeout ?? 0

  useEffect(() => {
    const id = setTimeout(() => setIsOver(true), delay)
    return () => clearTimeout(id)
  }, [delay])

  return { isOver }
}
