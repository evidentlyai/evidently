import Box from '@material-ui/core/Box'
import LinearProgress from '@material-ui/core/LinearProgress'
import { useNavigation } from 'react-router-dom'

export const NavigationProgress = () => {
  const navigation = useNavigation()
  const isNavigation = navigation.state !== 'idle'

  return isNavigation ? <LinearProgress /> : <Box sx={{ height: '4px' }} />
}
