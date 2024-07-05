import type { CreateCRUD, ErrorData, ID, StrictID } from '~/api/types/utils'
import { ProjectModel, TestSuiteModel, ReportModel } from '~/api/types'

export type ProjectsProvider = CreateCRUD<ProjectModel> & {
  reloadSnapshots: (args: { project: ID }) => Promise<ErrorData | null>
  listReports: (args: { project: ID }) => Promise<StrictID<ReportModel>[]>
  listTestSuites: (args: { project: ID }) => Promise<StrictID<TestSuiteModel>[]>
  deleteSnapshot: (args: { project: ID; snapshot: ID }) => Promise<ErrorData | null>
}
