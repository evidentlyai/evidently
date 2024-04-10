import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
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

export default {
  path: 'projects/:projectId',
  lazy: async () => {
    const { ProjectTemplate, DEFAULT_PROJECT_TABS, ...rest } = await import(
      'evidently-ui-lib/routes-components/projectId'
    )

    const Component = () => <ProjectTemplate tabsConfig={DEFAULT_PROJECT_TABS} />

    return { Component, ...rest }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary,
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute]
} satisfies RouteObject
