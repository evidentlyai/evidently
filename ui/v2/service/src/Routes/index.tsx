import { RouteObject } from 'react-router-dom'

import HomeRoute from './home'
import ProjectsRoute from './projects/projectId'
import ProjectsListRoute from './projectsList'
import NotFound from './NotFound'

const homeRoute = {
  ...HomeRoute,

  ////////////////////
  // children routes
  ////////////////////

  children: [ProjectsListRoute, ProjectsRoute, NotFound]
} satisfies RouteObject

export const Routes = [homeRoute]
