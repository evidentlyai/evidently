import { VersionInfo } from '~/api'
import { VersionProvider } from '~/api/types/providers/version'
import { GetLoaderAction } from '~/utils'

export type LoaderData = VersionInfo

export const injectAPI: GetLoaderAction<VersionProvider, LoaderData> = ({ api }) => ({
  loader: () => api.getVersion()
})
