import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/projectId/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

////////////////////
// children routes
////////////////////

import DashboardRoute from './dashboard'
import ReportsRoute from './reports'
import TestSuitesRoute from './test-suites'

const PROJECT_TABS = [
  { id: 'dashboard', link: '.', label: 'Dashboard' },
  { id: 'reports', link: 'reports', label: 'Reports' },
  { id: 'test_suites', link: 'test-suites', label: 'Test suites' },
  { id: 'comparisons', link: 'comparisons', disabled: true, label: 'Comparisons' }
]

export default {
  path: 'projects/:projectId',
  lazy: async () => {
    const { ProjectTemplate, ...rest } = await import(
      'evidently-ui-lib/routes-components/projectId'
    )

    const Component = () => <ProjectTemplate tabsConfig={PROJECT_TABS} />

    return { Component, ...rest }
  },
  loader,
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute]
} satisfies RouteObject
