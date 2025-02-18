import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'

import type { GetRouteByPath } from '~/routes/types'

import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import {
  ProjectDashboard,
  getDataRange,
  getValidDate,
  useDashboardFilterParamsDebounced
} from 'evidently-ui-lib/routes-components/dashboard'
import {
  type DashboardFilterQueryParams,
  getProjectDashboard
} from 'evidently-ui-lib/routes-components/dashboard/data'

import { DashboardWidgets } from 'evidently-ui-lib/components/DashboardWidgets'
import {
  HintOnHoverToPlot,
  type PlotMouseEventType
} from 'evidently-ui-lib/components/OnClickedPoint'
import { Box, Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import { RouterLink } from '~/routes/components'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/?index'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

export const loadData = ({
  params,
  query
}: loadDataArgs<{ queryKeys: DashboardFilterQueryParams }>) => {
  const { projectId } = params as Params

  return getProjectDashboard({ api: clientAPI, projectId, query })
}

export const Component = () => {
  const { loaderData: data, query, setQuery } = useCurrentRouteParams<CurrentRoute>()

  const dateRange = getDataRange(data)

  const { dates, setDates } = useDashboardFilterParamsDebounced({
    dates: {
      dateFrom: getValidDate(query.timestamp_start) ?? dateRange.minDate,
      dateTo: getValidDate(query.timestamp_end) ?? dateRange.maxDate
    },
    onDebounce: (newDate) => {
      setQuery(
        {
          timestamp_start: getValidDate(newDate.dateFrom)?.format('YYYY-MM-DDTHH:mm') ?? undefined,
          timestamp_end: getValidDate(newDate.dateTo)?.format('YYYY-MM-DDTHH:mm') ?? undefined
        },
        {
          replace: true,
          preventScrollReset: true
        }
      )
    }
  })

  return (
    <ProjectDashboard
      Widgets={<DashboardWidgets widgets={data.widgets} />}
      dateFilterProps={{ dates, setDates, dateRange }}
      OnClickedPointComponent={GoToSnapshotByPoint}
      OnHoveredPlotComponent={HintOnHoverToPlot}
    />
  )
}

const GoToSnapshotByPoint = ({ event }: { event: PlotMouseEventType }) => {
  const p = event.points[0]
  const customdata = p.customdata as Partial<
    Record<'test_fingerprint' | 'metric_fingerprint' | 'snapshot_id', string>
  >

  const { projectId } = useParams() as Params

  if (!customdata || !customdata.snapshot_id) {
    return <></>
  }

  const snapshot_type = 'metric_fingerprint' in customdata ? 'report' : 'test-suite'

  const linkToSnapshot = `/projects/:projectId/${snapshot_type}s/:snapshotId` as const

  return (
    <>
      <Box
        sx={{
          position: 'absolute',
          bottom: 0,
          right: 0,
          p: 1,
          background: (t) => t.palette.background.default,
          borderRadius: '10px'
        }}
      >
        <Stack direction={'row'} alignItems={'center'} gap={2}>
          <RouterLink
            type='button'
            to={linkToSnapshot}
            title={`View ${snapshot_type.split('-').join(' ')}`}
            variant='outlined'
            paramsToReplace={{ projectId, snapshotId: customdata.snapshot_id }}
          />
        </Stack>
      </Box>
    </>
  )
}
