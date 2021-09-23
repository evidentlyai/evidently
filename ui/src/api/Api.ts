import {Layout, PlotData} from "plotly.js";

export class Result<T> {
    constructor(result?: T, error?: string) {
        this.result = result;
        this.error = error;
    }

    result?: T;
    error?: string;

    Ok = (result: T) => new Result<T>(result, undefined);
    Error = (error: string) => new Result<T>(undefined, error);
}

export interface GraphWidgetParams
{
}

export interface TableWidgetParams
{
    header: string[];
    data: (number | string)[][];
}

export interface CounterInfo {
    value: number;
    label: string;
}

export interface CounterWidgetParams
{
    counters: CounterInfo[];
}

export interface PercentWidgetParams
{
    value: number;
    maxValue: number;
    details?: string;
}

export interface BigGraphWidgetParams
{
    data: Partial<PlotData>[];
    layout: Partial<Layout>;
}

export interface TabGraph
{
    id: string;
    title: string;
    graph: BigGraphWidgetParams;
}

export interface MultiTabGraphWidgetParams
{
    graphs: TabGraph[];
}

export interface TabWidget {
    id: string;
    title: string;
    widget: WidgetInfo;
}

export interface MultiTabWidgetParams
{
    tabs: TabWidget[];
}

export interface WidgetGroupParams
{
    widgets: WidgetInfo[];
}

export enum WidgetSize
{
    Small,
    Medium,
    Big,
}

export interface AlertStats {
    active: number;
    triggered: {
        period: number;
        last_24h: number;
    }
}

export interface MetricAlertParams {
    value: string | number;
    state?: "info" | "success" | "warning" | "error";
    text: string;
    longText: string;
}

export interface InsightsParams {
    title: string;
    severity: "info" | "warning" | "error" | "success";
    text: string;
}

export interface GraphOptions {
    color: string;
}

export interface LineGraphOptions {
    xField: string;
    yField: string;
}

export interface ScatterGraphOptions {
    xField: string;
    yField: string;
}

export interface HistogramGraphOptions {
    xField: string;
    yField: string;
}

export interface ColumnDefinition {
    title: string;
    field: string;
    sort?: "asc" | "desc";
    type?: "line" | "scatter" | "histogram";
    options?: LineGraphOptions | ScatterGraphOptions | HistogramGraphOptions;
}

export interface BigTableRowDetails {
    parts: {"title": string, "id": string, "type": string}[];
    insights: InsightsParams[];
}

export type BigTableDataRow = any & {graphId?: string, details?: BigTableRowDetails}

export interface BigTableWidgetParams {
    columns: ColumnDefinition[];
    data: BigTableDataRow[];
    showInfoColumn: boolean;
    rowsPerPage?: number;
}

export interface WidgetInfo {
    type: string;
    title: string;
    size: WidgetSize;
    details?: string;
    params: PercentWidgetParams
        | BigGraphWidgetParams
        | TableWidgetParams
        | CounterWidgetParams
        | WidgetGroupParams
        | MultiTabGraphWidgetParams
        | BigTableWidgetParams
    ;
    alertsPosition?: "row" | "column";
    alertStats?: AlertStats;
    alerts?: MetricAlertParams[];
    insights?: InsightsParams[];
}

export type AdditionalGraphInfo = BigGraphWidgetParams

export interface DashboardInfo
{
    name: string;
    widgets: WidgetInfo[];
}


export interface SectionInfo {
    id: string;
    name: string;
    sections?: SectionInfo[];
    disabled: boolean;
}

export interface ProjectInfo {
    id: string;
    title: string;
    test_project: boolean;
    sections: SectionInfo[];
}

export interface Api {
    getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo>
    getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo>
    getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo>
    getProjects(): Promise<ProjectInfo[]>
}