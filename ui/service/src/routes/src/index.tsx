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
import { DatasetView } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/dataset-view/import'
import { DialogView } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/dialog-view/import'
import { ExportId } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/import'
import { IndexRedirect } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/index-redirect/import'
import { TraceView } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/trace-view/import'
import { TracesLayout } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/import'
import { IndexTracesList } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/index-traces-list/import'

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
                  } as const),

                  Route(TracesLayout, {
                    path: 'traces',
                    children: [
                      Route(IndexTracesList, { index: true } as const),
                      Route(ExportId, {
                        path: ':exportId',
                        children: [
                          Route(IndexRedirect, { index: true } as const),
                          Route(DatasetView, { path: 'dataset' } as const),
                          Route(TraceView, { path: 'trace' } as const),
                          Route(DialogView, { path: 'dialog' } as const)
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
    ]
  } as const)
] as const satisfies RouteExtended[]
