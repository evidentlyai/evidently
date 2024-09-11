import { useState } from 'react'

import { Box, CircularProgress, Typography } from '@mui/material'

interface LoadableViewProps<T> {
  children?: (params: T) => JSX.Element
  func: () => Promise<T>
}

enum LoadState {
  Uninitialized = 0,
  Initialized = 1,
  Loading = 2,
  Loaded = 3,
  Failed = 4
}

interface LoadableViewState<T> {
  status: LoadState
  func: () => Promise<T>
  result?: T
}

const LoadableView = <T,>({ func, children }: LoadableViewProps<T>): JSX.Element => {
  const [state, setState] = useState<LoadableViewState<T>>(() => ({
    status: LoadState.Uninitialized,
    func
  }))

  if (state.status === LoadState.Uninitialized) {
    setState((prevState) => ({ ...prevState, status: LoadState.Initialized }))
  }

  if (state.status === LoadState.Initialized) {
    setState((prevState) => ({ ...prevState, status: LoadState.Loading }))

    state
      .func()
      .then((result) => setState((prev) => ({ ...prev, status: LoadState.Loaded, result })))
      .catch(() => setState((prev) => ({ ...prev, status: LoadState.Failed })))
  }

  return (
    <>
      {state.status === LoadState.Loaded ? (
        children && state.result && children(state.result)
      ) : state.status === LoadState.Failed ? (
        <Typography align='center'>Failed</Typography>
      ) : state.status === LoadState.Loading ? (
        <Box textAlign='center'>
          <CircularProgress />
        </Box>
      ) : null}
    </>
  )
}

export default LoadableView
