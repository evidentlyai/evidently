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

  return <CustomProgress isProgress={isNavigation} />
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

const CustomProgress = ({ isProgress }: { isProgress?: boolean }) => {
  return (
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 1000 }}>
      <Box
        height={2}
        sx={[
          {
            background: 'linear-gradient(90deg, #ed0500 0%, #FF1BE1 70%)',
            transitionProperty: 'width',
            transitionTimingFunction: 'cubic-bezier(0.22, 0.61, 0.36, 1);'
          },
          { width: 0 },
          Boolean(isProgress) && { transitionDuration: '10s', width: 0.8 }
        ]}
      />
    </Box>
  )
}
