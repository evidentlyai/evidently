import { useNavigation } from 'react-router-dom'
import { Box, LinearProgress } from '@mui/material'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const isNavigation = navigation.state !== 'idle'

  if (isNavigation) {
    return <LinearProgress sx={{ height: 4, position: 'sticky', top: 0 }} />
  }

  return <Box sx={{ height: 4 }} />
}
