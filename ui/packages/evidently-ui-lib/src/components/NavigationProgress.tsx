import { useFetchers, useNavigation } from 'react-router-dom'
import { Box, LinearProgress } from '@mui/material'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const fetchers = useFetchers()

  const isNavigation = navigation.state !== 'idle' || fetchers.some(({ state }) => state !== 'idle')

  if (!isNavigation) {
    return null
  }

  return (
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 99922343 }}>
      <LinearProgress sx={{ height: '3px' }} />
    </Box>
  )
}
