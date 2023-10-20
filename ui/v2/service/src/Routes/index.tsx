import { RouteObject } from 'react-router-dom'

import HomeRoute from './home'
import ProjectsRoute from './projects/projectId'
import ProjectsListRoute from './projectsList'

const homeRoute = {
  ...HomeRoute,
  children: [ProjectsListRoute, ProjectsRoute]
} satisfies RouteObject

export const Routes = [homeRoute]
