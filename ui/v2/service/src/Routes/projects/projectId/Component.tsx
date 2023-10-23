import { Alert, Box, Collapse, Grid, IconButton, Link, Tab, Tabs, Typography } from '@mui/material'

import {
  Link as RouterLink,
  Outlet,
  useMatches,
  LoaderFunctionArgs,
  useLoaderData,
  ShouldRevalidateFunction
} from 'react-router-dom'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { crumbFunction } from 'Components/BreadCrumbs'
import { isOnlySearchParamsChanges } from 'Utils/isOnlySearchParamsChanges'

const PROJECT_TABS = [
  { id: 'dashboard', link: '.' },
  { id: 'reports', link: 'reports' },
  { id: 'test_suites', link: 'test-suites', label: 'Test suites' },
  { id: 'comparisons', link: 'comparisons', disabled: true }
]

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.name || 'undefined' })
}

export function ErrorBoundary() {
  return (
    <Collapse sx={{ my: 3 }} unmountOnExit in={true}>
      <Alert severity="error">
        <Typography variant="h6">Something went wrong...</Typography>
      </Alert>
    </Collapse>
  )
}

export const shouldRevalidate: ShouldRevalidateFunction = (args) => {
  if (isOnlySearchParamsChanges(args)) {
    return false
  }

  return true
}

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { projectId } = params
  invariant(projectId, 'missing projectId')

  return api.getProjectInfo(projectId)
}

export const Component = () => {
  const matches = useMatches()
  const project = useLoaderData() as loaderData
  const tabIndex = PROJECT_TABS.findIndex((tab) => matches.find(({ id }) => id === tab.id))

  return (
    <Box mt={2}>
      <Grid container spacing={2} direction="row" justifyContent="flex-start" alignItems="flex-end">
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

      <Tabs value={tabIndex} aria-label="simple tabs example" indicatorColor={'primary'}>
        {PROJECT_TABS.map((tab) => {
          const TabComponent = (
            <Tab label={tab.label || tab.id} value={tab.id} disabled={tab.disabled} />
          )
          if (tab.disabled) {
            return TabComponent
          }

          return (
            <Link component={RouterLink} to={tab.link}>
              {TabComponent}
            </Link>
          )
        })}
      </Tabs>
      <Outlet />
    </Box>
  )
}
