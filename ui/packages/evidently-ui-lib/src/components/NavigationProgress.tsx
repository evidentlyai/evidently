import { useNavigation } from 'react-router-dom'
import { Box, LinearProgress } from '@mui/material'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const isNavigation = navigation.state !== 'idle' || fetchers.some((f) => f.state !== 'idle')

  if (isNavigation) {
    return <LinearProgress sx={{ height: 4, position: 'sticky', top: 0, left: 0, zIndex: 999 }} />
  }

  return <Box sx={{ height: 4 }} />
}
