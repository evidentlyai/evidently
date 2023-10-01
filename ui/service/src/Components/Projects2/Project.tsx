import { Grid, IconButton, Link, Tab, Tabs, Typography } from '@material-ui/core'

import { Link as RouterLink, Outlet, useParams, useMatches } from 'react-router-dom'
import FilterNoneIcon from '@material-ui/icons/FilterNone'
import invariant from 'tiny-invariant'

export const PROJECT_TABS = [
  { id: 'dashboard', link: '.' },
  { id: 'reports', link: 'reports' },
  { id: 'test_suites', link: 'test-suites', label: 'Test suites' },
  { id: 'comparisons', link: 'comparisons', disabled: true }
]

export const Project = () => {
  const { projectId } = useParams()
  const matches = useMatches()

  const tabIndex = PROJECT_TABS.findIndex((tab) => matches.find(({ id }) => id === tab.id))

  invariant(projectId, 'missing projectId')

  return (
    <>
      <Grid container spacing={2} direction="row" justifyContent="flex-start" alignItems="flex-end">
        <Grid item xs={12}>
          <Typography style={{ color: '#aaa' }} variant="body2">
            {`project id: ${projectId}`}
            <IconButton
              size="small"
              style={{ marginLeft: 10 }}
              onClick={() => navigator.clipboard.writeText(projectId)}
            >
              <FilterNoneIcon />
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
    </>
  )
}
