import type { DashboardInfoModel } from '~/api/types'

import { JSONParseExtended } from '~/api/JsonParser'
import { type API, responseParser } from '~/api/client-heplers'

export const getProjectDashboard = ({
  api,
  project_id,
  timestamp_start,
  timestamp_end
}: API & { project_id: string; timestamp_start: string | null; timestamp_end: string | null }) => {
  return api
    .GET('/api/projects/{project_id}/dashboard', {
      params: {
        path: { project_id },
        query: { timestamp_start, timestamp_end }
      },
      parseAs: 'text'
    })
    .then(responseParser())
    .then(JSONParseExtended<DashboardInfoModel>)
}
