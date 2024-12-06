import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

import {
  decorateAllRoutes,
  decorateTopLevelRoutes,
  provideCrumb
} from 'evidently-ui-lib/router-utils/utils'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './src/snapshot-view/import'

import { DashboardLazy } from './src/dashboard/import'

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
            path: 'reports',
            ...provideCrumb({ title: 'Reports' }),
            children: [
              { index: true, ...ReportsList },
              { path: ':snapshotId', ...SnapshotIdLazy }
            ]
          },
          {
            path: 'test-suites',
            ...provideCrumb({ title: 'Test suites' }),
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

const finalRoutes = routes.map(decorateTopLevelRoutes).map((r) => decorateAllRoutes(r))

export const router = createBrowserRouter(finalRoutes)
