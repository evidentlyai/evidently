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
    .then(({ name, id }) => ({ name, id }))
}

const TABS = {
  reports: 'reports',
  'test-suites': 'test-suites',
  index: 'index'
}

export const Component = () => {
  const { loaderData: project, params } = useRouteParams<CurrentRoute>()
  const isReports = useMatchRouter({ path: '/:projectId/reports' })
  const isTestSuites = useMatchRouter({ path: '/:projectId/test-suites' })

  const { projectId } = params

  const selectedTab = isReports ? TABS.reports : isTestSuites ? TABS['test-suites'] : TABS.index

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

      <Tabs value={selectedTab} aria-label='simple tabs example' indicatorColor={'primary'}>
        <RouterLink
          type='tab'
          value={TABS.index}
          label={'Dashboard'}
          to='/:projectId/?index'
          paramsToReplace={{ projectId }}
        />

        <RouterLink
          type='tab'
          value={TABS.reports}
          label={'Reports'}
          to='/:projectId/reports'
          paramsToReplace={{ projectId }}
        />

        <RouterLink
          type='tab'
          value={TABS['test-suites']}
          label={'Test suites'}
          to='/:projectId/test-suites'
          paramsToReplace={{ projectId }}
        />
      </Tabs>

      <Outlet />
    </Box>
  )
}
