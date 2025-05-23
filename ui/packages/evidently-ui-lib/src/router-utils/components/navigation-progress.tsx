import { Box, CircularProgress, LinearProgress } from '@mui/material'
import { useFetchers, useNavigation, useRevalidator } from 'react-router-dom'

export const NavigationProgressWithFetchers = () => {
  const navigation = useNavigation()
  const fetchers = useFetchers()
  const { state } = useRevalidator()

  const isNavigation =
    navigation.state !== 'idle' ||
    fetchers.some(({ state }) => state !== 'idle') ||
    state !== 'idle'

  if (!isNavigation) {
    return null
  }

  return (
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 1000 }}>
      <LinearProgress sx={{ height: '3px' }} />
    </Box>
  )
}

export const NavigationProgress = () => {
  const navigation = useNavigation()

  const isNavigation = navigation.state !== 'idle'

  if (!isNavigation) {
    return null
  }

  return (
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 1000 }}>
      <LinearProgress sx={{ height: '3px' }} />
    </Box>
  )
}

export const FetchersProgress = () => {
  const fetchers = useFetchers()
  const { state } = useRevalidator()

  const isNavigation = fetchers.some(({ state }) => state !== 'idle') || state !== 'idle'

  if (!isNavigation) {
    return null
  }

  return (
    <>
      <CircularProgress color='warning' size={15} />
    </>
  )
}
