import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

import { decorateAllRoutes, decorateTopLevelRoutes } from 'evidently-ui-lib/router-utils/utils'

import { Dashboard } from './src/dashboard/import'
import { Home } from './src/home/import'
import { Project } from './src/project/import'
import { ProjectsList } from './src/projects-list/import'
import { Reports } from './src/reports/import'

export const routes = [
  {
    ...Home,
    children: [
      { index: true, ...ProjectsList },
      {
        path: ':projectId',
        ...Project,
        children: [
          { index: true, ...Dashboard },
          { path: 'reports', ...Reports }
        ]
      }
    ]
  }
] as const satisfies RouteExtended[]

export const _router = createBrowserRouter(
  [...routes].map(decorateTopLevelRoutes).map(decorateAllRoutes)
)
