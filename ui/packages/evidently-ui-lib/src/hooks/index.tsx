import React from 'react'
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
