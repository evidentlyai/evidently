import { components } from '~/api/types/schema'
import type { CreateCRUD, ID } from '~/api/types/utils'

///////////////////////////////
///  TYPES
///////////////////////////////
type Schemas = components['schemas']

export type Project = Schemas['Project']
export type DashboardInfoModel = Schemas['DashboardInfoModel']

///////////////////////////////
///  CRUDS
///////////////////////////////

export type ProjectsCRUD = CreateCRUD<Project>
export type DashboardCRUD = {
  get(args: {
    project: ID
    options: {
      timestamp_start?: null | string
      timestamp_end?: null | string
    }
  }): Promise<DashboardInfoModel>
}

///////////////////////////////
///  API
///////////////////////////////

export interface API {
  projects: ProjectsCRUD
  dashboard: DashboardCRUD
}
