import { Box, Typography } from '@mui/material'
import { RouteObject } from 'react-router-dom'

export default {
  path: '*',
  Component: () => {
    return (
      <Box display={'flex'} justifyContent={'center'}>
        <Typography variant="h4">Page Not Found</Typography>
      </Box>
    )
  }
} satisfies RouteObject
