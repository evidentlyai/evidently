import type { CreateCRUD, ID, StrictID } from '~/api/types/utils'
import { ProjectModel, TestSuiteModel, ReportModel } from '~/api/types'

export type ProjectsProvider = CreateCRUD<ProjectModel> & {
  reloadSnapshots: (args: { project: ID }) => Promise<null>
  listReports: (args: { project: ID }) => Promise<StrictID<ReportModel>[]>
  listTestSuites: (args: { project: ID }) => Promise<StrictID<TestSuiteModel>[]>
}
