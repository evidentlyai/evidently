import { Alert, Box, Collapse, Grid, IconButton, Link, Tab, Tabs, Typography } from '@mui/material'

import { Link as RouterLink, Outlet, useMatches, useLoaderData, useRouteError } from 'react-router-dom'
import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { crumbFunction } from '~/components/BreadCrumbs'
import { loaderData } from './data'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.name || 'undefined' })
}

export function ErrorBoundary() {
  const error = useRouteError()

  return (
    <Collapse sx={{ my: 3 }} unmountOnExit in={true}>
      <Alert severity="error">
        <Typography variant="h6">Something went wrong...</Typography>
        <Typography>{String(error)}</Typography>
      </Alert>
    </Collapse>
  )
}

export const ProjectTemplate = ({
  tabsConfig
}: {
  tabsConfig: { id: string; link: string; label?: string; disabled?: boolean }[]
}) => {
  const matches = useMatches()
  const project = useLoaderData() as loaderData
  const tabIndex = tabsConfig.findIndex((tab) => matches.find(({ id }) => id === tab.id))

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
        {tabsConfig.map((tab) => {
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
