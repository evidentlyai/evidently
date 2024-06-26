import dayjs from 'dayjs'
import invariant from 'tiny-invariant'
import { GetLoaderAction } from '~/api/utils'

export type LoaderData = DashboardInfoModel

import { FILTER_QUERY_PARAMS } from '~/components/DashboardDateFilter'
import { DashboardInfoModel } from '~/api/types'
import { DashboardProvider } from '~/api/types/providers/dashboard'

export const getLoaderAction: GetLoaderAction<DashboardProvider, LoaderData> = ({ api }) => ({
  loader: ({ params, request }) => {
    invariant(params.projectId, 'missing projectId')

    const { searchParams } = new URL(request.url)

    let timestamp_start = searchParams.get(FILTER_QUERY_PARAMS.FROM)
    let timestamp_end = searchParams.get(FILTER_QUERY_PARAMS.TO)

    if (timestamp_start && !dayjs(timestamp_start).isValid()) {
      timestamp_start = null
    }

    if (timestamp_end && !dayjs(timestamp_end).isValid()) {
      timestamp_end = null
    }

    return api.getProjectDashboard({
      project: { id: params.projectId },
      options: {
        timestamp_start,
        timestamp_end
      }
    })
  }
})
