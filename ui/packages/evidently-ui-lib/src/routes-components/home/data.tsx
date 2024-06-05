import { VersionModel } from '~/api/types'
import { VersionProvider } from '~/api/types/providers/version'
import { GetLoaderAction } from '~/utils'

export type LoaderData = VersionModel

export const getLoaderAction: GetLoaderAction<VersionProvider, LoaderData> = ({ api }) => ({
  loader: () => api.getVersion()
})
