import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ensureID } from 'evidently-ui-lib/api/utils'
import { ProjectLayoutTemplate } from 'evidently-ui-lib/components/Project/ProjectLayout'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Tabs } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import { ProjectContext } from '~/contexts/project'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'
import { useMatchRouter } from '~/routes/type-safe-route-helpers/hooks'
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
  const {
    loaderData: { project },
    params
  } = useCurrentRouteParams<CurrentRoute>()

  const isReports = useMatchRouter({ path: '/projects/:projectId/reports' })
  const isDatasets = useMatchRouter({ path: '/projects/:projectId/datasets' })

  const { projectId } = params

  const selectedTab = isReports ? TABS.reports : isDatasets ? TABS.datasets : TABS.index

  return (
    <ProjectContext.Provider value={{ project }}>
      <ProjectLayoutTemplate project={project}>
        <>
          <Tabs value={selectedTab} aria-label='simple tabs example' indicatorColor={'primary'}>
            <RouterLink
              type='tab'
              value={TABS.index}
              label={'Dashboard'}
              to='/projects/:projectId/?index'
              paramsToReplace={{ projectId }}
            />

            <RouterLink
              type='tab'
              value={TABS.reports}
              label={'Reports'}
              to='/projects/:projectId/reports'
              paramsToReplace={{ projectId }}
            />

            <RouterLink
              type='tab'
              value={TABS.datasets}
              label={'Datasets'}
              to='/projects/:projectId/datasets'
              paramsToReplace={{ projectId }}
            />
          </Tabs>

          <Outlet />
        </>
      </ProjectLayoutTemplate>
    </ProjectContext.Provider>
  )
}

const TABS = { reports: 'reports', index: 'index', datasets: 'datasets' }
