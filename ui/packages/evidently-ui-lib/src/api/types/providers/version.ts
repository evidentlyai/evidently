import { VersionModel } from '~/api/types'

export type VersionProvider = {
  getVersion(): Promise<VersionModel>
}
