import type { BackendPaths, BackendV2Paths } from 'evidently-ui-lib/api/types'
import { createClient } from 'evidently-ui-lib/shared-dependencies/openapi-fetch'

export const clientAPIV2 = createClient<BackendV2Paths>({ baseUrl: '/' })
export const clientAPI = createClient<BackendPaths>({ baseUrl: '/' })
