import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { RouteExtended } from 'evidently-ui-lib/router-utils/types'

import { decarateTopLevelRoute, decorateAllRoute } from 'evidently-ui-lib/router-utils/utils'
import { Home } from './src/home/import'
import { Project } from './src/project/import'
import { ProjectsList } from './src/projects-list/import'

export const routes = [
  {
    path: '',
    ...Home,
    children: [
      { index: true, ...ProjectsList },
      {
        path: ':projectId',
        ...Project
      }
    ]
  }
] as const satisfies RouteExtended[]

export const _router = createBrowserRouter(
  [...routes].map(decarateTopLevelRoute).map(decorateAllRoute)
)
