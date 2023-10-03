import HomeRoute from './home'
import ProjectsRoute from './projects/:projectId'
import ProjectsListRoute from './projectsList'

const homeRoute = {
  ...HomeRoute,
  children: [ProjectsListRoute, ProjectsRoute]
}

export const Routes = [homeRoute]
