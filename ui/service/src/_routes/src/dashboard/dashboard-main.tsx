import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { LoaderFunctionArgs } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { GetRouteByPath } from '~/_routes/types'

import { useLocalStorage } from 'evidently-ui-lib/hooks/index'
import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { ProjectDashboard } from 'evidently-ui-lib/routes-components/dashboard'
import { getProjectDashboard } from 'evidently-ui-lib/routes-components/dashboard/data'
import {
  getDateFromSearchForAPI,
  useDashboardFilterPropsFromSearchParamsDebounced
} from 'evidently-ui-lib/routes-components/dashboard/router'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId/?index'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

export const loader = ({ params /* request */, request }: LoaderFunctionArgs) => {
  const { projectId: project_id } = params as Params

  const { searchParams } = new URL(request.url)

  const { timestamp_start, timestamp_end } = getDateFromSearchForAPI(searchParams)

  return getProjectDashboard({
    api: clientAPI,
    project_id,
    timestamp_start,
    timestamp_end
  })
}

export const Component = () => {
  const { loaderData: data } = useRouteParams<CurrentRoute>()

  const { min_timestamp, max_timestamp } = data

  const dateFilterProps = useDashboardFilterPropsFromSearchParamsDebounced({
    min_timestamp,
    max_timestamp
  })

  const [isXaxisAsCategorical, setIsXaxisAsCategorical] = useLocalStorage('some-key', false)

  return (
    <ProjectDashboard
      data={data}
      dateFilterProps={dateFilterProps}
      showInOrderProps={{ isXaxisAsCategorical, setIsXaxisAsCategorical }}
    />
  )
}
