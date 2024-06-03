import createClient from 'openapi-fetch'
import { json } from 'react-router-dom'
import { API } from '~/api/types'
import { JSONParseExtended } from '~/api/JsonParser'

import { DashboardInfoModel } from '~/api/types'

import type { BackendPaths } from '~/api/types'
import type { ErrorResponse, JSONStrExtended } from '~/api/types/utils'

const client = createClient<BackendPaths>({ baseUrl: '/' })

export const apiV2: API = {
  projects: {
    async list() {
      const { data, error, response } = await client.GET('/api/projects')

      if (error) {
        // @ts-ignore
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return data
    },
    async update({ body }) {
      const { data, error } = await client.POST('/api/projects/{project_id}/info', {
        params: { path: { project_id: body.id } },
        body: body
      })

      if (error) {
        return { error }
      }

      return data
    },
    async get({ id }) {
      const { data, error, response } = await client.GET('/api/projects/{project_id}/info', {
        params: { path: { project_id: id } }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return data
    },
    async delete({ id }) {
      const { error } = await client.DELETE('/api/projects/{project_id}', {
        params: { path: { project_id: id } }
      })

      if (error) {
        return { error }
      }

      return null
    },
    async create({ body }) {
      const { data, error } = await client.POST('/api/projects', { body })

      if (error) {
        return { error }
      }

      return data
    },
    dashboard: {
      async get({ project, options }) {
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
      }
    }
  }
}
