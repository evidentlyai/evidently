import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser.ts'
import { responseParser } from 'evidently-ui-lib/api/client-heplers.ts'
import type { DashboardModel } from 'evidently-ui-lib/api/types'
import { DrawDashboardPanels } from 'evidently-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { DashboardViewParamsContext } from 'evidently-ui-lib/contexts/DashboardViewParamsV2'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { PanelComponent } from '~/Components/DashboardPanel'
import { OnClickedPointComponent } from '~/Components/GoToSnapshotButton'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/?index'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = { title: 'Dashboard' }
export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = ({ params, query }: loadDataArgs) => {
  const { projectId } = params as Params

  return clientAPI
    .GET('/api/v2/dashboards/{project_id}', {
      params: { path: { project_id: projectId }, query },
      parseAs: 'text'
    })
    .then(responseParser())
    .then(JSONParseExtended<DashboardModel>)
}

export const Component = () => {
  const { loaderData: data } = useCurrentRouteParams<CurrentRoute>()

  return (
    <Box py={2}>
      <DashboardViewParamsContext.Provider value={{ OnClickedPointComponent }}>
        <DrawDashboardPanels PanelComponent={PanelComponent} panels={data.panels} />
      </DashboardViewParamsContext.Provider>
    </Box>
  )
}
