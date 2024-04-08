import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'

import {
  RouteObject,
  createBrowserRouter
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import HomeRoute from './home'
import ProjectsRoute from './projects/projectId'
import ProjectsListRoute from './projectsList'
import NotFound from './NotFound'

const homeRoute = {
  ...HomeRoute,

  ////////////////////
  // children routes
  ////////////////////

  children: [ProjectsListRoute, ProjectsRoute, NotFound],
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject

export const router = createBrowserRouter([homeRoute])
