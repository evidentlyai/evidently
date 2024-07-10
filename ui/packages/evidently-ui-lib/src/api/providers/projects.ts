import { json } from 'react-router-dom'
import createClient from 'openapi-fetch'

import type { ProjectsProvider } from '~/api/types/providers/projects'
import type { BackendPaths } from '~/api/types'
import type { ErrorResponse } from '~/api/types/utils'

import { ensureID } from '~/api/utils'

export const getProjectsProvider: (baseUrl?: string) => ProjectsProvider = (baseUrl) => {
  const client = createClient<BackendPaths>({ baseUrl })

  return {
    async list() {
      const { data, error, response } = await client.GET('/api/projects')

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return data.map(ensureID)
    },
    async update({ body }) {
      const { data, error } = await client.POST('/api/projects/{project_id}/info', {
        params: { path: { project_id: body.id } },
        body: body
      })

      if (error) {
        return { error }
      }

      return ensureID(data)
    },
    async get({ id }) {
      const { data, error, response } = await client.GET('/api/projects/{project_id}/info', {
        params: { path: { project_id: id } }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return ensureID(data)
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

      return ensureID(data)
    },
    async reloadSnapshots({ project }) {
      const { error } = await client.GET('/api/projects/{project_id}/reload', {
        params: { path: { project_id: project.id } }
      })

      if (error) {
        return { error }
      }

      return null
    },
    async deleteSnapshot({ project, snapshot }) {
      const { error } = await client.DELETE('/api/projects/{project_id}/{snapshot_id}', {
        params: { path: { project_id: project.id, snapshot_id: snapshot.id } }
      })

      if (error) {
        return { error }
      }

      return null
    },
    async listReports({ project }) {
      const { data, error, response } = await client.GET('/api/projects/{project_id}/reports', {
        params: { path: { project_id: project.id } }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return data.map(ensureID)
    },
    async listTestSuites({ project }) {
      const { data, error, response } = await client.GET('/api/projects/{project_id}/test_suites', {
        params: { path: { project_id: project.id } }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
      }

      return data.map(ensureID)
    }
  }
}
