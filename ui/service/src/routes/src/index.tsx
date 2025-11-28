import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

// It's important to import `SnapshotIdRoute` before `DashboardRoute`. Affects bundle chunks
import { SnapshotIdRoute } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/snapshot-view/import'

import { IndexDashboardRoute } from './home/projects-crumb-prefix/projects-layout/project/index-dashboard/import'

import { Route } from 'evidently-ui-lib/router-utils/router-builder'
import { HomeRoute } from './home/import'
import { ProjectsCrumbPrefixRoute } from './home/projects-crumb-prefix/import'
import { IndexProjectsListRoute } from './home/projects-crumb-prefix/index-projects-list/import'
import { ProjectsLayoutRoute } from './home/projects-crumb-prefix/projects-layout/import'
import { DatasetIdRoute } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/dataset-id/import'
import { DatasetsLayoutRoute } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/import'
import { IndexDatasetsListRoute } from './home/projects-crumb-prefix/projects-layout/project/datasets-layout/index-datasets-list/import'
import { ProjectRoute } from './home/projects-crumb-prefix/projects-layout/project/import'
import { LoadPanelPointsAPIRoute } from './home/projects-crumb-prefix/projects-layout/project/load-panel-points/import'
import { CreateNewPromptRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/create-new-prompt/import'
import { PromptsRouteLayout } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/import'
import { IndexPromptsListRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/index-prompts-list/import'
import { PromptIdRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/promptId/import'
import { IndexSelectActionsRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/promptId/index-select-actions/import'
import { ManagePromptVersionsRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/promptId/manage-prompt-versions/import'
import { PromptIdCreateNewVersionRoute } from './home/projects-crumb-prefix/projects-layout/project/prompts-layout/promptId/new-prompt-version/import'
import { ReportsLayoutRoute } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/import'
import { IndexReportsListRoute } from './home/projects-crumb-prefix/projects-layout/project/reports-layout/index-reports-list/import'
import { DatasetViewRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/dataset-view/import'
import { DialogViewRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/dialog-view/import'
import { ExportIdRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/import'
import { IndexTracingExportIdRedirectRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/index-redirect/import'
import { TraceViewRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/exportId/trace-view/import'
import { TracesLayoutRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/import'
import { IndexTracesListRoute } from './home/projects-crumb-prefix/projects-layout/project/traces-layout/index-traces-list/import'

export const routes = [
  Route(HomeRoute, {
    children: [
      Route(ProjectsCrumbPrefixRoute, {
        children: [
          Route(IndexProjectsListRoute, { index: true } as const),

          Route(ProjectsLayoutRoute, {
            path: 'projects',
            children: [
              Route(ProjectRoute, {
                path: ':projectId',
                children: [
                  // Dashboard
                  Route(IndexDashboardRoute, { index: true } as const),

                  Route(LoadPanelPointsAPIRoute, { path: 'load-panel-points' } as const),

                  // Reports
                  Route(ReportsLayoutRoute, {
                    path: 'reports',
                    children: [
                      Route(IndexReportsListRoute, { index: true } as const),
                      Route(SnapshotIdRoute, { path: ':snapshotId' } as const)
                    ]
                  } as const),

                  // Datasets
                  Route(DatasetsLayoutRoute, {
                    path: 'datasets',
                    children: [
                      Route(IndexDatasetsListRoute, { index: true } as const),
                      Route(DatasetIdRoute, { path: ':datasetId' } as const)
                    ]
                  } as const),

                  // Traces
                  Route(TracesLayoutRoute, {
                    path: 'traces',
                    children: [
                      Route(IndexTracesListRoute, { index: true } as const),
                      Route(ExportIdRoute, {
                        path: ':exportId',
                        children: [
                          Route(IndexTracingExportIdRedirectRoute, { index: true } as const),
                          Route(DatasetViewRoute, { path: 'dataset' } as const),
                          Route(TraceViewRoute, { path: 'trace' } as const),
                          Route(DialogViewRoute, { path: 'dialog' } as const)
                        ]
                      } as const)
                    ]
                  } as const),

                  // Prompts
                  Route(PromptsRouteLayout, {
                    path: 'prompts',
                    children: [
                      Route(IndexPromptsListRoute, { index: true } as const),
                      Route(CreateNewPromptRoute, { path: 'new' } as const),

                      Route(PromptIdRoute, {
                        path: ':promptId',
                        children: [
                          Route(IndexSelectActionsRoute, { index: true } as const),
                          Route(ManagePromptVersionsRoute, { path: 'manage' } as const),
                          Route(PromptIdCreateNewVersionRoute, { path: 'new-version' } as const)
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
