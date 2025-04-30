import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser.ts'
import { responseParser } from 'evidently-ui-lib/api/client-heplers.ts'
import type { DashboardModel } from 'evidently-ui-lib/api/types/v2'
import { DrawDashboardPanels } from 'evidently-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { DashboardViewParamsContext } from 'evidently-ui-lib/contexts/DashboardViewParamsV2'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Box, Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { PanelComponent } from '~/Components/DashboardPanel'
import { clientAPI } from '~/api'
import { RouterLink } from '~/routes/components'
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

const GoToSnapshotByPoint = ({ snapshotId }: { snapshotId: string }) => {
  const { projectId } = useParams() as Params

  const linkToSnapshot = '/projects/:projectId/reports/:snapshotId' as const

  return (
    <>
      <Box style={{ marginRight: 10 }}>
        <Stack direction={'row'} alignItems={'end'} justifyContent={'end'} gap={2}>
          <RouterLink
            type='button'
            to={linkToSnapshot}
            title='View Report'
            variant='outlined'
            paramsToReplace={{ projectId, snapshotId }}
          />
        </Stack>
      </Box>
    </>
  )
}

export const Component = () => {
  const { loaderData: data } = useCurrentRouteParams<CurrentRoute>()

  return (
    <Box py={2}>
      <DashboardViewParamsContext.Provider
        value={{
          isXaxisAsCategorical: true,
          OnClickedPointComponent: GoToSnapshotByPoint
        }}
      >
        <DrawDashboardPanels PanelComponent={PanelComponent} panels={data.panels} />
      </DashboardViewParamsContext.Provider>
    </Box>
  )
}
