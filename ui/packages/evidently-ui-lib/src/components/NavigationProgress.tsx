import { useNavigation } from 'react-router-dom'
import { Box, LinearProgress } from '@mui/material'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const isNavigation = navigation.state !== 'idle'

  return isNavigation ? <LinearProgress sx={{ height: 4 }} /> : <Box sx={{ height: 4 }} />
}
