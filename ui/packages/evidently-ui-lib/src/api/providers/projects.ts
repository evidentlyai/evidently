import { json } from 'react-router-dom'
import createClient from 'openapi-fetch'

import type { ProjectsProvider } from '~/api/types/providers/projects'
import type { BackendPaths } from '~/api/types'
import { ErrorResponse, StrictID } from '~/api/types/utils'

const ensureID: <Entity extends { id?: string | null | undefined }>(
  e: Entity
) => StrictID<Entity> = (e) => {
  if (e.id) {
    return { ...e, id: e.id }
  }

  throw 'id is undefinded'
}

export const getProjectsProvider: (baseUrl?: string) => ProjectsProvider = (baseUrl) => {
  const client = createClient<BackendPaths>({ baseUrl })

  return {
    async list() {
      const { data, error, response } = await client.GET('/api/projects')

      if (error) {
        throw json(error satisfies ErrorResponse, {
          // @ts-ignore
          status: response.status
        })
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
      const { error, response } = await client.GET('/api/projects/{project_id}/reload', {
        params: { path: { project_id: project.id } }
      })

      if (error) {
        throw json(error satisfies ErrorResponse, { status: response.status })
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
