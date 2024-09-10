import { Box, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

export default {
  path: '*',
  Component: () => {
    return (
      <Box display={'flex'} justifyContent={'center'}>
        <Typography variant='h4'>Page Not Found</Typography>
      </Box>
    )
  }
} satisfies RouteObject
