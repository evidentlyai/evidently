import { Link, Tab, Tabs } from '@mui/material'
import { Outlet, Link as RouterLink, useLoaderData, useMatches } from 'react-router-dom'

import type { crumbFunction } from '~/components/BreadCrumbs'
import { ProjectLayoutTemplate } from '~/components/ProjectLayout'
import type { LoaderData } from './data'

export const handle: { crumb: crumbFunction<LoaderData> } = {
  crumb: (data, { pathname }) => ({ to: pathname, linkText: data?.project?.name || 'undefined' })
}

export const Component = () => {
  const { project } = useLoaderData() as LoaderData

  return (
    <ProjectLayoutTemplate project={project}>
      <>
        <ProjectTabs tabsConfig={PROJECT_TABS} />
        <Outlet />
      </>
    </ProjectLayoutTemplate>
  )
}

const ProjectTabs = ({
  tabsConfig = []
}: { tabsConfig?: { id: string; link: string; label?: string }[] }) => {
  const matches = useMatches()
  const tabIndex = tabsConfig.findIndex((tab) => matches.find(({ id }) => id === tab.id))

  return (
    <Tabs value={tabIndex} aria-label='simple tabs example' indicatorColor={'primary'}>
      {tabsConfig.map((tab) => (
        <Link key={tab.id} component={RouterLink} to={tab.link}>
          <Tab label={tab.label || tab.id} value={tab.id} />
        </Link>
      ))}
    </Tabs>
  )
}

const PROJECT_TABS = [
  { id: 'dashboard', link: '.', label: 'Dashboard' },
  { id: 'reports', link: 'reports', label: 'Reports' },
  { id: 'test_suites', link: 'test-suites', label: 'Test suites' }
]
