import { Version } from '~/api/types'

export type VersionProvider = {
  getVersion(): Promise<Version>
}
