import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { decarateTopLevelRoute, decorateAllRoute } from '~/_routes/utils'
import { Home } from './src/home/import'
import { ProjectsList } from './src/projectsList/import'
import type { RouteExtended } from './types'

export const routes = [
  { path: '', ...Home, children: [{ index: true, ...ProjectsList }] }
] as const satisfies RouteExtended[]

export const _router = createBrowserRouter(
  [...routes].map(decarateTopLevelRoute).map(decorateAllRoute)
)
