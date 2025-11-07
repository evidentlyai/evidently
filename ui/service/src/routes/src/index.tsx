import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

// It's important to import `SnapshotIdLazy` before `DashboardLazy`. Affects bundle chunks
import { SnapshotIdLazy } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/snapshot-view/import'

import { IndexDashboardLazy } from './home/projects-crumb-prefix/projects-layout/project/index-dashboard/import'

import { Route } from 'evidently-ui-lib/router-utils/router-builder'
import { Home } from './home/import'
import { ProjectsCrumbPrefixRoute } from './home/projects-crumb-prefix/import'
import { IndexProjectsList } from './home/projects-crumb-prefix/index-projects-list/import'
import { ProjectsLayout } from './home/projects-crumb-prefix/projects-layout/import'
import { DatasetId } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/dataset-id/import'
import { DatasetsLayout } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/import'
import { IndexDatasetsList } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/index-datasets-list/import'
import { Project } from './home/projects-crumb-prefix/projects-layout/project/import'
import { LoadPanelPointsAPIV2 } from './home/projects-crumb-prefix/projects-layout/project/load-panel-points/import'
import { ReportsLayout } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/import'
import { IndexReportsList } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/index-reports-list/import'

export const routes = [
  Route(Home, {
    children: [
      Route(ProjectsCrumbPrefixRoute, {
        children: [
          Route(IndexProjectsList, { index: true } as const),
          Route(ProjectsLayout, {
            path: 'projects',
            children: [
              Route(Project, {
                path: ':projectId',
                children: [
                  Route(IndexDashboardLazy, { index: true } as const),
                  Route(LoadPanelPointsAPIV2, { path: 'load-panel-points' } as const),
                  Route(ReportsLayout, {
                    path: 'reports',
                    children: [
                      Route(IndexReportsList, { index: true } as const),
                      Route(SnapshotIdLazy, { path: ':snapshotId' } as const)
                    ]
                  } as const),
                  Route(DatasetsLayout, {
                    path: 'datasets',
                    children: [
                      Route(IndexDatasetsList, { index: true } as const),
                      Route(DatasetId, { path: ':datasetId' } as const)
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
