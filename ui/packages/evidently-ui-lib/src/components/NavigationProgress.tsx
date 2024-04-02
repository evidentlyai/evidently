import { useFetchers, useNavigation } from 'react-router-dom'
import { Box, LinearProgress } from '@mui/material'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const fetchers = useFetchers()
  const isNavigation = navigation.state !== 'idle' || fetchers.some(({ state }) => state !== 'idle')

  if (isNavigation) {
    return <LinearProgress sx={{ height: 1, position: 'sticky', top: 0, left: 0, zIndex: 999 }} />
  }

  return <Box sx={{ height: 1 }} />
}
