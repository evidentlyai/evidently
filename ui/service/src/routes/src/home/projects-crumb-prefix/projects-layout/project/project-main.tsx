import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ensureID } from 'evidently-ui-lib/api/utils'
import { ProjectLayoutTemplate } from 'evidently-ui-lib/components/Project/ProjectLayout'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import { ProjectContext } from '~/contexts/project'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = {
  keyFromLoaderData: 'projectName' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId: project_id } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/info', { params: { path: { project_id } } })
    .then(responseParser())
    .then(ensureID)
    .then((project) => ({ project, projectName: project.name }))
}

export const Component = () => {
  const { loaderData } = useCurrentRouteParams<CurrentRoute>()
  const { project } = loaderData

  return (
    <ProjectContext.Provider value={{ project }}>
      <ProjectLayoutTemplate project={project}>
        <Outlet />
      </ProjectLayoutTemplate>
    </ProjectContext.Provider>
  )
}
