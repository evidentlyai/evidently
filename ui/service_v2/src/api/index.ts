import type { BackendPaths } from 'evidently-ui-lib/api/types/v2'
import { createClient } from 'evidently-ui-lib/shared-dependencies/openapi-fetch'

export const clientAPI = createClient<BackendPaths>({ baseUrl: '/' })
