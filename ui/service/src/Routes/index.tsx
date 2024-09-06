import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'

import {
  type RouteObject,
  createBrowserRouter
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import NotFound from './NotFound'
import HomeRoute from './home'
import ProjectsRoute from './projects/projectId'
import ProjectsListRoute from './projectsList'

const homeRoute = {
  ...HomeRoute,

  ////////////////////
  // children routes
  ////////////////////

  children: [ProjectsListRoute, ProjectsRoute, NotFound],
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject

export const router = createBrowserRouter([homeRoute])
