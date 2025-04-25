import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser.ts'
import { responseParser } from 'evidently-ui-lib/api/client-heplers.ts'
import type { DashboardModel } from 'evidently-ui-lib/api/types/v2'
import { DrawDashboardPanels } from 'evidently-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { PanelComponent } from '~/Components/DashboardPanel'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/?index'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

const loadDashboardAPI = '/api/v2/dashboards/{project_id}'
// type LoadDashboardAPIQuery = GetSearchParamsAPIs<'get'>[typeof loadDashboardAPI]

export const loadData = (
  { params, query }: loadDataArgs /* <{ queryKeys: keyof LoadDashboardAPIQuery }> */
) => {
  const { projectId } = params as Params

  return clientAPI
    .GET(loadDashboardAPI, { params: { path: { project_id: projectId }, query }, parseAs: 'text' })
    .then(responseParser())
    .then(JSONParseExtended<DashboardModel>)
}

export const Component = () => {
  const { loaderData: data } = useCurrentRouteParams<CurrentRoute>()

  return (
    <Box py={2}>
      <DrawDashboardPanels PanelComponent={PanelComponent} panels={data.panels} />
    </Box>
  )
}
