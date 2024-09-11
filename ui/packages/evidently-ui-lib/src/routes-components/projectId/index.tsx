import { Box, Grid, IconButton, Link, Tab, Tabs, Typography } from '@mui/material'

import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { Outlet, Link as RouterLink, useLoaderData, useMatches } from 'react-router-dom'
import type { crumbFunction } from '~/components/BreadCrumbs'
import type { LoaderData } from './data'

export const handle: { crumb: crumbFunction<LoaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.name || 'undefined' })
}

export const ProjectTemplate = ({
  tabsConfig = []
}: {
  tabsConfig?: { id: string; link: string; label?: string }[]
}) => {
  const matches = useMatches()
  const project = useLoaderData() as LoaderData
  const tabIndex = tabsConfig.findIndex((tab) => matches.find(({ id }) => id === tab.id))

  return (
    <Box mt={2}>
      <Grid container spacing={2} direction='row' justifyContent='flex-start' alignItems='flex-end'>
        <Grid item xs={12}>
          <Typography sx={{ color: '#aaa' }} variant='body2'>
            {`project id: ${project.id}`}
            <IconButton
              size='small'
              style={{ marginLeft: 10 }}
              onClick={() => {
                navigator.clipboard.writeText(project.id)
              }}
            >
              <ContentCopyIcon fontSize='small' />
            </IconButton>
          </Typography>
        </Grid>
      </Grid>

      {tabsConfig.length > 0 && (
        <Tabs value={tabIndex} aria-label='simple tabs example' indicatorColor={'primary'}>
          {tabsConfig.map((tab) => (
            <Link key={tab.id} component={RouterLink} to={tab.link}>
              <Tab label={tab.label || tab.id} value={tab.id} />
            </Link>
          ))}
        </Tabs>
      )}
      <Outlet />
    </Box>
  )
}

const PROJECT_TABS = [
  { id: 'dashboard', link: '.', label: 'Dashboard' },
  { id: 'reports', link: 'reports', label: 'Reports' },
  { id: 'test_suites', link: 'test-suites', label: 'Test suites' }
]

export const Component = () => <ProjectTemplate tabsConfig={PROJECT_TABS} />
export const ProjectWithoutTabs = () => <ProjectTemplate />
