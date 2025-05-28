import { Box, CircularProgress, LinearProgress } from '@mui/material'
import { useEffect, useState } from 'react'
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

  return <CustomProgress isProgress={navigation.state !== 'idle'} />
}

export const FetchersProgress = () => {
  const fetchers = useFetchers()
  const { state } = useRevalidator()

  const isNavigation = fetchers.some(({ state }) => state !== 'idle') || state !== 'idle'

  if (!isNavigation) {
    return null
  }

  return <CircularProgress color='warning' size={15} />
}

const CustomProgress = ({ isProgress }: { isProgress: boolean }) => {
  const [isProgressProxy, setIsProgressProxy] = useState(false)
  const [progressJustFinished, setProgressJustFinished] = useState(false)

  if (!isProgressProxy && isProgress) {
    setIsProgressProxy(true)
  }

  if (isProgressProxy && !isProgress) {
    setIsProgressProxy(false)
    setProgressJustFinished(true)
  }

  useEffect(() => {
    if (progressJustFinished) {
      setTimeout(() => setProgressJustFinished(false), 500)
    }
  }, [progressJustFinished])

  return (
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 1000 }}>
      <Box
        height={2}
        sx={[
          {
            background: 'linear-gradient(90deg, #ed0500 0%, #FF1BE1 70%)',
            transitionProperty: 'width'
          },
          { width: 0 },
          isProgressProxy && {
            width: 0.8,
            transitionDuration: '10s',
            transitionTimingFunction: 'cubic-bezier(0.22, 0.61, 0.36, 1)'
          },
          progressJustFinished && {
            width: 1,
            transitionDuration: '0.4s',
            transitionTimingFunction: 'linear'
          }
        ]}
      />
    </Box>
  )
}
