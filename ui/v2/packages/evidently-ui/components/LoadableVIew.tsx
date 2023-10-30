import React, { useEffect, useState } from 'react'

import { Box, CircularProgress } from '@mui/material'

interface LoadableViewProps<T> {
  children?: (params: T) => React.ReactNode
  func: () => Promise<T>
}

enum LoadState {
  Uninitialized,
  Initialized,
  Loading,
  Loaded,
  Failed
}

interface LoadableViewState<T> {
  status: LoadState
  func?: () => Promise<T>
  result?: T
}

const LoadableView = <T,>(props: LoadableViewProps<T>) => {
  const [state, setState] = useState<LoadableViewState<T>>(() => ({
    status: LoadState.Uninitialized
  }))
  useEffect(() => {
    setState({ status: LoadState.Initialized, func: props.func })
  }, [props.func])
  if (state.status === LoadState.Initialized) {
    setState((prevState) => ({ ...prevState, status: LoadState.Loading }))
    state.func!().then((res) =>
      setState((s) => {
        return { status: LoadState.Loaded, func: s.func, result: res }
      })
    )
  }

  return (
    <React.Fragment>
      {state.status === LoadState.Loaded ? (
        props.children ? (
          props.children(state.result!)
        ) : (
          <div />
        )
      ) : (
        <Box textAlign="center">
          <CircularProgress />
        </Box>
      )}
    </React.Fragment>
  )
}

export default LoadableView
