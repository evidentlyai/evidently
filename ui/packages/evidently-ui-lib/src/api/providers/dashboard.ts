import { json } from 'react-router-dom'
import createClient from 'openapi-fetch'

import { JSONParseExtended } from '~/api/JsonParser'
import type { BackendPaths, DashboardInfoModel } from '~/api/types'
import type { ErrorResponse, JSONStrExtended } from '~/api/types/utils'
import type { DashboardProvider } from '~/api/types/providers/dashboard'

export const getDashboardProvider: (baseUrl?: string) => DashboardProvider = (baseUrl) => {
  const client = createClient<BackendPaths>({ baseUrl })

  return {
    async getProjectDashboard({ project, options }) {
      const { data, error, response } = await client.GET('/api/projects/{project_id}/dashboard', {
        parseAs: 'text',
        params: {
          path: { project_id: project.id },
          query: {
            timestamp_start: options.timestamp_start,
            timestamp_end: options.timestamp_end
          }
        }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return JSONParseExtended<DashboardInfoModel>(data satisfies JSONStrExtended)
    },
    async getSnapshotDashboard({ project, snapshot }) {
      const { data, error, response } = await client.GET(
        '/api/projects/{project_id}/{snapshot_id}/data',
        {
          parseAs: 'text',
          params: {
            path: { project_id: project.id, snapshot_id: snapshot.id }
          }
        }
      )

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return JSONParseExtended<DashboardInfoModel>(data satisfies JSONStrExtended)
    },
    async getDashboardGraph({ project, snapshot, graph }) {
      const { data, error, response } = await client.GET(
        '/api/projects/{project_id}/{snapshot_id}/graphs_data/{graph_id}',
        {
          parseAs: 'text',
          params: {
            path: { project_id: project.id, snapshot_id: snapshot.id, graph_id: graph.id }
          }
        }
      )

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return JSONParseExtended<any>(data satisfies JSONStrExtended)
    }
  }
}
