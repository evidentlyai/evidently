import dayjs from 'dayjs'
import invariant from 'tiny-invariant'
import type { GetLoaderAction } from '~/api/utils'

export type LoaderData = DashboardInfoModel

import type { DashboardInfoModel } from '~/api/types'
import { FILTER_QUERY_PARAMS } from '~/components/DashboardDateFilter'

import { JSONParseExtended } from '~/api/JsonParser'
import { type API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'

export const getLoaderAction: GetLoaderAction<API_CLIENT_TYPE, LoaderData> = ({ api }) => ({
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

    return api
      .GET('/api/projects/{project_id}/dashboard', {
        params: {
          path: { project_id: params.projectId },
          query: { timestamp_start, timestamp_end }
        },
        parseAs: 'text'
      })
      .then(responseParser())
      .then(JSONParseExtended<DashboardInfoModel>)
  }
})
