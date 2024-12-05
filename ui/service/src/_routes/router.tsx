import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

import { decorateAllRoutes, decorateTopLevelRoutes } from 'evidently-ui-lib/router-utils/utils'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './src/snapshot-view/import'

import { DashboardLazy } from './src/dashboard/import'

import { PrefixRoute } from './src/_prefix'
import { Home } from './src/home/import'
import { Project } from './src/project/import'
import { ProjectsList } from './src/projects-list/import'
import { ReportsList } from './src/reports-list/import'
import { TestSuitesList } from './src/test-suites-list/import'

export const routes = [
  {
    ...Home,
    children: [
      { index: true, ...ProjectsList },
      {
        path: ':projectId',
        ...Project,
        children: [
          { index: true, ...DashboardLazy },
          {
            ...PrefixRoute({ prefix: 'reports', crumbTitle: 'Reports' } as const),
            children: [
              { index: true, ...ReportsList },
              { path: ':snapshotId', ...SnapshotIdLazy }
            ]
          },
          {
            ...PrefixRoute({ prefix: 'test-suites', crumbTitle: 'Test Suites' } as const),
            children: [
              { index: true, ...TestSuitesList },
              { path: ':snapshotId', ...SnapshotIdLazy }
            ]
          }
        ]
      }
    ]
  }
] as const satisfies RouteExtended[]

export const _router = createBrowserRouter(
  [...routes].map(decorateTopLevelRoutes).map(decorateAllRoutes)
)
