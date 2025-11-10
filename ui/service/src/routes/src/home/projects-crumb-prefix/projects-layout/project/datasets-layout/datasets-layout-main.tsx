import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/datasets'

const crumb: CrumbDefinition = { title: 'Datasets' }

export const handle = { crumb }

export const Component = () => (
  <Box mt={2}>
    <Outlet />
  </Box>
)
