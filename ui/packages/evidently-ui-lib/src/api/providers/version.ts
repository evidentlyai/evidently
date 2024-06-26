import { json } from 'react-router-dom'
import createClient from 'openapi-fetch'

import type { BackendPaths } from '~/api/types'
import type { ErrorResponse } from '~/api/types/utils'
import type { VersionProvider } from '~/api/types/providers/version'

export const getVersionProvider: (baseUrl?: string) => VersionProvider = (baseUrl) => {
  const client = createClient<BackendPaths>({ baseUrl })

  return {
    async getVersion() {
      const { data, error, response } = await client.GET('/api/version')

      if (error) {
        throw json(error satisfies ErrorResponse, {
          // @ts-ignore
          status: response.status
        })
      }

      return data
    }
  }
}
