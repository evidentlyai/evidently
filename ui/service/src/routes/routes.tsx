import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './src/snapshot-view/import'

import { DashboardLazy } from './src/dashboard/import'

import { Route } from 'evidently-ui-lib/router-utils/utils'
import { Home } from './src/home/import'
import { Project } from './src/project/import'
import { ProjectsList } from './src/projects-list/import'
import { ReportsLayout } from './src/reports-layout/import'
import { ReportsList } from './src/reports-list/import'
import { TestSuitesLayout } from './src/test-suites-layout/import'
import { TestSuitesList } from './src/test-suites-list/import'

export const routes = [
  Route(Home, {
    children: [
      Route(ProjectsList, { index: true } as const),
      Route(Project, {
        path: ':projectId',
        children: [
          Route(DashboardLazy, { index: true } as const),
          Route(ReportsLayout, {
            path: 'reports',
            children: [
              Route(ReportsList, { index: true } as const),
              Route(SnapshotIdLazy, { path: ':snapshotId' } as const)
            ]
          } as const),
          Route(TestSuitesLayout, {
            path: 'test-suites',
            children: [
              Route(TestSuitesList, { index: true } as const),
              Route(SnapshotIdLazy, { path: ':snapshotId' } as const)
            ]
          } as const)
        ]
      } as const)
    ]
  } as const)
] as const satisfies RouteExtended[]
