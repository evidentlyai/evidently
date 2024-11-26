import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { LoaderFunctionArgs } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { useRouteParams } from '~/_routes/hooks'
import type { GetRouteByPath } from '~/_routes/types'

import { DashboardParams } from 'evidently-ui-lib/components/DashboardDateFilter'
import { DashboardWidgets } from 'evidently-ui-lib/components/DashboardWidgets'
import { DashboardViewParamsContext } from 'evidently-ui-lib/contexts/DashboardViewParams'
import { useDashboardParams } from 'evidently-ui-lib/routes-components/dashboard'
import { getProjectDashboard } from 'evidently-ui-lib/routes-components/dashboard/data'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId/?index'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

export const loader = ({ params, request }: LoaderFunctionArgs) => {
  const { projectId: project_id } = params as Params

  return getProjectDashboard({ api: clientAPI, project_id, request })
}

export const Component = () => {
  const { loaderData: data } = useRouteParams<CurrentRoute>()

  const { dataRanges, isShowDateFilter, isDashboardHideDates, setIsDashboardHideDates } =
    useDashboardParams(data)

  return (
    <>
      <DashboardParams
        dataRanges={dataRanges}
        isShowDateFilter={isShowDateFilter}
        isDashboardHideDates={isDashboardHideDates}
        setIsDashboardHideDates={setIsDashboardHideDates}
      />

      <DashboardViewParamsContext.Provider value={{ isXaxisAsCategorical: isDashboardHideDates }}>
        <DashboardWidgets widgets={data.widgets} />
      </DashboardViewParamsContext.Provider>
    </>
  )
}
