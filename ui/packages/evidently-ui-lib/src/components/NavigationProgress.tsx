import { Box, LinearProgress } from '@mui/material'
import { useFetchers, useNavigation, useRevalidator } from 'react-router-dom'

export const NavigationProgress = () => {
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
    <Box width={1} sx={{ position: 'fixed', top: 0, left: 0, zIndex: 99999 }}>
      <LinearProgress sx={{ height: '3px' }} />
    </Box>
  )
}
