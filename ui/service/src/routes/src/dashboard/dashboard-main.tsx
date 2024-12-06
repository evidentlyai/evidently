import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { GetRouteByPath } from '~/routes/types'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
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

import { GoToSnapshotByPoint, HintOnHoverToPlot } from 'evidently-ui-lib/components/OnClickedPoint'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId/?index'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

export const loaderSpecial = ({
  params,
  query
}: LoaderSpecialArgs<{ queryKeys: DashboardFilterQueryParams }>) => {
  const { projectId } = params as Params

  return getProjectDashboard({ api: clientAPI, projectId, query })
}

export const Component = () => {
  const { loaderData: data, query, setQuery } = useRouteParams<CurrentRoute>()

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
      data={data}
      dateFilterProps={{ dates, setDates, dateRange }}
      OnClickedPointComponent={GoToSnapshotByPoint}
      OnHoveredPlotComponent={HintOnHoverToPlot}
    />
  )
}
