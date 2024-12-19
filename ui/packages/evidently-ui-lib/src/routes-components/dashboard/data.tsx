import type { DashboardInfoModel, GetSearchParamsAPIs } from '~/api/types'

import { JSONParseExtended } from '~/api/JsonParser'
import { type API, responseParser } from '~/api/client-heplers'

const api_path = '/api/projects/{project_id}/dashboard'

export type ProjectDashboardSearchParams = GetSearchParamsAPIs<'get'>[typeof api_path]
export type DashboardFilterQueryParams = keyof ProjectDashboardSearchParams

export const getProjectDashboard = ({
  api,
  projectId,
  query
}: API & { projectId: string; query: ProjectDashboardSearchParams }) =>
  api
    .GET(api_path, { params: { path: { project_id: projectId }, query }, parseAs: 'text' })
    .then(responseParser())
    .then(JSONParseExtended<DashboardInfoModel>)
