import { Layout, PlotData } from 'plotly.js-cartesian-dist-min'

export class Result<T> {
  constructor(result?: T, error?: string) {
    this.result = result
    this.error = error
  }

  result?: T
  error?: string

  Ok = (result: T) => new Result<T>(result, undefined)
  Error = (error: string) => new Result<T>(undefined, error)
}

export interface GraphWidgetParams {}

export interface TableWidgetParams {
  header: string[]
  data: (number | string)[][]
}

export interface CounterInfo {
  value: number
  label: string
}

export interface CounterWidgetParams {
  counters: CounterInfo[]
}

export interface PercentWidgetParams {
  value: number
  maxValue: number
  details?: string
}

export interface BigGraphWidgetParams {
  data: Partial<PlotData>[]
  layout: Partial<Layout>
}

export interface TabGraph {
  id: string
  title: string
  graph: BigGraphWidgetParams
}

export interface MultiTabGraphWidgetParams {
  graphs: TabGraph[]
}

export interface TabWidget {
  id: string
  title: string
  widget: WidgetInfo
}

export interface MultiTabWidgetParams {
  tabs: TabWidget[]
}

export interface WidgetGroupParams {
  widgets: WidgetInfo[]
}

export interface WidgetListParams {
  widgets: WidgetInfo[]
  pageSize: number
}

export enum WidgetSize {
  Small,
  Medium,
  Big
}

export interface AlertStats {
  active: number
  triggered: {
    period: number
    last_24h: number
  }
}

export interface MetricAlertParams {
  value: string | number
  state?: 'info' | 'success' | 'warning' | 'error'
  text: string
  longText: string
}

export interface InsightsParams {
  title: string
  severity: 'info' | 'warning' | 'error' | 'success'
  text: string
}

export interface GraphOptions {
  color: string
}

export interface LineGraphOptions {
  xField: string
  yField: string
  color: string
}

export interface ScatterGraphOptions {
  xField: string
  yField: string
  color: string
}

export interface HistogramGraphOptions {
  xField: string
  yField: string
  color: string
}

export interface ColumnDefinition {
  title: string
  field: string
  sort?: 'asc' | 'desc'
  type?: 'line' | 'scatter' | 'histogram'
  options?: LineGraphOptions | ScatterGraphOptions | HistogramGraphOptions
}

export interface DetailsPart {
  title: string
  id: string
  type: string
}

export interface BigTableRowDetails {
  parts: DetailsPart[]
  insights: InsightsParams[]
}

export type BigTableDataRow = any & { graphId?: string; details?: BigTableRowDetails }

export interface BigTableWidgetParams {
  columns: ColumnDefinition[]
  data: BigTableDataRow[]
  showInfoColumn: boolean
  rowsPerPage?: number
}

export interface Metric {
  label: string
  values: (string | number)[]
}

export interface RichDataParams {
  header: string
  description: string
  metrics: Metric[]
  metricsValuesHeaders: string[]
  graph?: BigGraphWidgetParams
  details?: BigTableRowDetails
}

export interface TextWidgetParams {
  text: string
}

export type TestState = 'unknown' | 'error' | 'success' | 'warning' | 'fail'

export interface TestDataInfo {
  title: string
  description: string
  state: TestState
  groups: any
  details?: BigTableRowDetails
}

export interface TestGroupData {
  id: string
  title: string
  description?: string
  sortIndex?: number
  severity?: TestState
}

export interface TestGroupTypeData {
  id: string
  title: string
  values: TestGroupData[]
}

export interface TestSuiteWidgetParams {
  tests: TestDataInfo[]
  testGroupTypes: TestGroupTypeData[]
}

export interface WidgetInfo {
  id: string
  type: string
  title: string
  size: WidgetSize
  details?: string
  params:
    | PercentWidgetParams
    | BigGraphWidgetParams
    | TableWidgetParams
    | CounterWidgetParams
    | WidgetGroupParams
    | MultiTabGraphWidgetParams
    | BigTableWidgetParams
    | RichDataParams
    | TextWidgetParams
    | TestSuiteWidgetParams
  alertsPosition?: 'row' | 'column'
  alertStats?: AlertStats
  alerts?: MetricAlertParams[]
  insights?: InsightsParams[]
}

export type AdditionalGraphInfo = BigGraphWidgetParams

type DashboardTab = { id: string; title: string }

export interface DashboardInfo {
  name: string
  widgets: WidgetInfo[]
  max_timestamp: string | null
  min_timestamp: string | null
}

export interface SectionInfo {
  id: string
  name: string
  sections?: SectionInfo[]
  disabled: boolean
}

export interface ProjectInfo {
  id: string
  name: string
  description?: string
  date_from?: string
  date_to?: string
  team_id?: string
}

export interface ProjectDetails extends ProjectInfo {
  dashboard: { tabs: DashboardTab[]; tab_id_to_panel_ids: Record<string, string[]> }
}

export type MetadataValueType = Record<string, string | string[] | Record<string, string>>

export interface SnapshotInfo {
  id: string
  timestamp: string
  tags: string[]
  metadata: MetadataValueType
}

export interface VersionInfo {
  version: string
}

export interface Api {
  getAdditionalGraphData(
    projectId: string,
    dashboardId: string,
    graphId: string
  ): Promise<AdditionalGraphInfo>

  getAdditionalWidgetData(
    projectId: string,
    dashboardId: string,
    widgetId: string
  ): Promise<WidgetInfo>

  getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo>

  getProjectDashboard(
    projectId: string,
    from?: string | null,
    to?: string | null
  ): Promise<DashboardInfo>

  getReports(projectId: string): Promise<SnapshotInfo[]>

  getTestSuites(projectId: string): Promise<SnapshotInfo[]>

  getProjects(): Promise<ProjectInfo[]>

  getProjectInfo(projectId: string): Promise<ProjectDetails>

  createProject(project: Partial<ProjectDetails>): Promise<ProjectDetails>

  deleteProject(projectId: string): Promise<Response>

  getVersion(): Promise<VersionInfo>

  editProjectInfo(project: ProjectDetails): Promise<Response>

  reloadProject(projectId: string): Promise<Response>
}
