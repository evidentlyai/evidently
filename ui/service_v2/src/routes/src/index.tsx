import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './snapshot-view/import'

import { DashboardLazy } from './dashboard/import'

import { Route } from 'evidently-ui-lib/router-utils/router-builder'
import { LoadPanelPointsAPIV2 } from './api/load-panel-points/import'
import { Home } from './home/import'
import { Project } from './project/import'
import { ProjectsLayout } from './projects-layout/import'
import { ProjectsList } from './projects-list/import'
import { ReportsLayout } from './reports-layout/import'
import { ReportsList } from './reports-list/import'
import { TestSuitesLayout } from './test-suites-layout/import'
import { TestSuitesList } from './test-suites-list/import'

export const routes = [
  Route(Home, {
    children: [
      Route(LoadPanelPointsAPIV2, {
        path: 'v2/projects/:projectId/api/load-panel-points'
      } as const),
      Route(ProjectsList, { index: true } as const),
      Route(ProjectsLayout, {
        path: 'projects',
        children: [
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
    ]
  } as const)
] as const satisfies RouteExtended[]
