import type { CreateCRUD, ID } from '~/api/types/utils'
import { Project, TestSuiteModel, ReportModel } from '~/api/types'

export type ProjectsProvider = CreateCRUD<Project> & {
  reloadSnapshots: (args: { project: ID }) => Promise<void>
  listReports: (args: { project: ID }) => Promise<ReportModel[]>
  listTestSuites: (args: { project: ID }) => Promise<TestSuiteModel[]>
}
