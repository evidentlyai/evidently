import {
  Box,
  Divider,
  Grid,
  IconButton,
  Link,
  Stack,
  Tab,
  Tabs,
  Tooltip,
  Typography
} from '@mui/material'

import { Link as RouterLink, Outlet, useMatches, useLoaderData } from 'react-router-dom'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'

import DashboardIcon from '@mui/icons-material/Dashboard'
import ChecklistIcon from '@mui/icons-material/Checklist'
import SummarizeIcon from '@mui/icons-material/Summarize'

import { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.name || 'undefined' })
}

export const DEFAULT_PROJECT_TABS = [
  { id: 'dashboard', link: '.', label: 'Dashboard', icon: <DashboardIcon fontSize="large" /> },
  { id: 'reports', link: 'reports', label: 'Reports', icon: <SummarizeIcon fontSize="large" /> },
  {
    id: 'test_suites',
    link: 'test-suites',
    label: 'Test suites',
    icon: <ChecklistIcon fontSize="large" />
  }
] as const

export const ProjectTemplate = ({
  tabsConfig
}: {
  tabsConfig: readonly { id: string; link: string; label: string; icon: React.ReactElement }[]
}) => {
  const matches = useMatches()
  const project = useLoaderData() as loaderData
  const tabIndex = tabsConfig.findIndex((tab) => matches.find(({ id }) => id === tab.id))

  return (
    <Box mt={2}>
      <Grid
        px={3}
        container
        spacing={2}
        direction="row"
        justifyContent="flex-start"
        alignItems="flex-end"
      >
        <Grid item xs={12}>
          <Typography sx={{ color: '#aaa' }} variant="body2">
            {`project id: ${project.id}`}
            <IconButton
              size="small"
              style={{ marginLeft: 10 }}
              onClick={() => navigator.clipboard.writeText(project.id)}
            >
              <ContentCopyIcon fontSize="small" />
            </IconButton>
          </Typography>
        </Grid>
      </Grid>

      <Stack direction={'row'} useFlexGap justifyContent={'space-between'}>
        <Box>
          <Tabs
            sx={{
              position: 'sticky',
              top: 0,
              left: 0
            }}
            orientation="vertical"
            value={tabIndex}
            indicatorColor={'primary'}
          >
            {tabsConfig.map((tab, index) => (
              <Tooltip placement="right" title={tab.label}>
                <Link component={RouterLink} to={tab.link}>
                  <Tab
                    sx={[
                      tabIndex === index && {
                        '& .MuiSvgIcon-root': {
                          color: 'secondary.main'
                        }
                      }
                    ]}
                    icon={tab.icon}
                  />
                </Link>
              </Tooltip>
            ))}
          </Tabs>
        </Box>
        <Divider flexItem orientation="vertical"></Divider>
        <Box width={1} px={5}>
          <Outlet />
        </Box>
      </Stack>
    </Box>
  )
}
