import { type API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import type { VersionModel } from '~/api/types'
import type { GetLoaderAction } from '~/api/utils'

export type LoaderData = VersionModel

export const getLoaderAction: GetLoaderAction<API_CLIENT_TYPE, LoaderData> = ({ api }) => ({
  loader: () => api.GET('/api/version').then(responseParser())
})
