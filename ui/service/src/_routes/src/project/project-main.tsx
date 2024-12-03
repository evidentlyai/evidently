import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ensureID } from 'evidently-ui-lib/api/utils'
import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import {
  Box,
  Grid,
  IconButton,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { ContentCopy as ContentCopyIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'

import type { GetRouteByPath } from '~/_routes/types'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = {
  keyFromLoaderData: 'name' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

export const loaderSpecial = ({ params }: LoaderSpecialArgs) => {
  const { projectId: project_id } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/info', { params: { path: { project_id } } })
    .then(responseParser())
    .then(ensureID)
}

export const Component = () => {
  const { loaderData: project } = useRouteParams<CurrentRoute>()

  return (
    <Box mt={2}>
      <Grid container spacing={2} direction='row' justifyContent='flex-start' alignItems='flex-end'>
        <Grid item xs={12}>
          <Typography sx={{ color: '#aaa' }} variant='body2'>
            {`project id: ${project.id}`}
            <IconButton
              size='small'
              style={{ marginLeft: 10 }}
              onClick={() => navigator.clipboard.writeText(project.id)}
            >
              <ContentCopyIcon fontSize='small' />
            </IconButton>
          </Typography>
        </Grid>
      </Grid>

      {/* {tabsConfig.length > 0 && (
      <Tabs value={tabIndex} aria-label='simple tabs example' indicatorColor={'primary'}>
        {tabsConfig.map((tab) => (
          <Link key={tab.id} component={RouterLink} to={tab.link}>
            <Tab label={tab.label || tab.id} value={tab.id} />
          </Link>
        ))}
      </Tabs>
    )} */}
      <Outlet />
    </Box>
  )
}
