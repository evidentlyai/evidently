import { VersionInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = VersionInfo

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: () => api.getVersion()
})
