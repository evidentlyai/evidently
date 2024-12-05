import type { GetParams, LoaderSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { GetRouteByPath } from '~/_routes/types'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import {
  ProjectDashboard,
  getDataRange,
  getValidDate,
  useDashboardFilterParamsDebounced
} from 'evidently-ui-lib/routes-components/dashboard'
import {
  type ProjectDashboardSearchParams,
  getProjectDashboard
} from 'evidently-ui-lib/routes-components/dashboard/data'

import { formatDate } from 'evidently-ui-lib/utils/index'
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
}: LoaderSpecialArgs<{ queryKeys: keyof ProjectDashboardSearchParams }>) => {
  const { projectId: project_id } = params as Params

  return getProjectDashboard({ api: clientAPI, project_id, query })
}

export const Component = () => {
  const { loaderData: data, query, setQuery } = useRouteParams<CurrentRoute>()

  const dateRange = getDataRange(data)

  const { dates, setDates } = useDashboardFilterParamsDebounced({
    dates: {
      dateFrom: getValidDate(query.timestamp_start) || dateRange.minDate,
      dateTo: getValidDate(query.timestamp_end) || dateRange.maxDate
    },
    onDebounce: (newDate) => {
      setQuery(
        {
          timestamp_start: formatDate(getValidDate(newDate.dateFrom)?.toDate()) ?? undefined,
          timestamp_end: formatDate(getValidDate(newDate.dateTo)?.toDate()) ?? undefined
        },
        {
          replace: true,
          preventScrollReset: true
        }
      )
    }
  })

  return <ProjectDashboard data={data} dateFilterProps={{ dates, setDates, dateRange }} />
}
