import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './snapshot-view/import'

import { DashboardLazy } from './dashboard/import'

import { Route } from 'evidently-ui-lib/router-utils/router-builder'
import { Home } from './home/import'
import { LoadPanelPointsAPIV2 } from './load-panel-points/import'
import { Project } from './project/import'
import { ProjectsCrumbPrefixRoute } from './projects-crumb-prefix/import'
import { ProjectsLayout } from './projects-layout/import'
import { ProjectsList } from './projects-list/import'
import { ReportsLayout } from './reports-layout/import'
import { ReportsList } from './reports-list/import'

export const routes = [
  Route(Home, {
    children: [
      Route(ProjectsCrumbPrefixRoute, {
        children: [
          Route(ProjectsList, { index: true } as const),
          Route(ProjectsLayout, {
            path: 'projects',
            children: [
              Route(Project, {
                path: ':projectId',
                children: [
                  Route(DashboardLazy, { index: true } as const),
                  Route(LoadPanelPointsAPIV2, { path: 'load-panel-points' } as const),
                  Route(ReportsLayout, {
                    path: 'reports',
                    children: [
                      Route(ReportsList, { index: true } as const),
                      Route(SnapshotIdLazy, { path: ':snapshotId' } as const)
                    ]
                  } as const)
                ]
              } as const)
            ]
          } as const)
        ]
      } as const)
    ]
  } as const)
] as const satisfies RouteExtended[]
