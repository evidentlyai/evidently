import dayjs from 'dayjs'
import invariant from 'tiny-invariant'
import { DashboardInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = DashboardInfo

import { FILTER_QUERY_PARAMS } from '~/components/DashboardDateFilter'

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params, request }) => {
    invariant(params.projectId, 'missing projectId')

    const { searchParams } = new URL(request.url)

    let date_from = searchParams.get(FILTER_QUERY_PARAMS.FROM)
    let date_to = searchParams.get(FILTER_QUERY_PARAMS.TO)

    if (date_from && !dayjs(date_from).isValid()) {
      date_from = null
    }

    if (date_to && !dayjs(date_to).isValid()) {
      date_to = null
    }

    return api.getProjectDashboard(params.projectId, date_from, date_to)
  }
})
