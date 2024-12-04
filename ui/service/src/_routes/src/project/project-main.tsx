import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ensureID } from 'evidently-ui-lib/api/utils'
import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import {
  Box,
  Grid,
  IconButton,
  Tabs,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { ContentCopy as ContentCopyIcon } from 'evidently-ui-lib/shared-dependencies/mui-icons-material'

import type { GetRouteByPath } from '~/_routes/types'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { RouterLink, useMatchRouter } from '~/_routes/components'
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
  const { loaderData: project, params } = useRouteParams<CurrentRoute>()
  const isReports = useMatchRouter({ path: '/:projectId/reports' })

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

      <Tabs
        value={isReports ? 'reports' : 'index'}
        aria-label='simple tabs example'
        indicatorColor={'primary'}
      >
        <RouterLink
          type='tab'
          value={'index'}
          label={'Dashboard'}
          to='/:projectId/?index'
          paramsToReplace={{ projectId: params.projectId }}
        />

        <RouterLink
          type='tab'
          value={'reports'}
          label={'reports'}
          to='/:projectId/reports'
          paramsToReplace={{ projectId: params.projectId }}
        />
      </Tabs>

      <Outlet />
    </Box>
  )
}
