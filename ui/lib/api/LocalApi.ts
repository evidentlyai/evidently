import {AdditionalGraphInfo, Api, DashboardInfo, ProjectInfo, ReportInfo, TestSuiteInfo, WidgetInfo} from "./Api";

export default class LocalApi implements Api {
    private readonly dashboard: DashboardInfo;
    private readonly projects: ProjectInfo[];
    private additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>;

    constructor(
        dashboard: DashboardInfo,
        additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>,
        projects?: ProjectInfo[]) {
        this.dashboard = dashboard;
        this.additionalGraphs = additionalGraphs;
        this.projects = projects ?? [];
    }

    async getProjectDashboard(projectId: string, from?: string, to?: string): Promise<DashboardInfo> {
        return {name: "Project Dasboard", widgets: []}
    }
    async getReports(projectId: string): Promise<ReportInfo[]> {
        return [{id: "report_1", timestamp: new Date(Date.now())}]
    }

    getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        var graph = this.additionalGraphs.get(graphId);
        return graph ? Promise.resolve(graph as AdditionalGraphInfo) : Promise.reject("No graph found");
    }

    getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo> {
        var graph = this.additionalGraphs.get(widgetId);
        return graph ? Promise.resolve(graph as WidgetInfo) : Promise.reject("No graph found");
    }

    getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        return Promise.resolve(this.dashboard);
    }

    getProjects(): Promise<ProjectInfo[]> {
        return Promise.resolve(this.projects);
    }

    getReport(projectId: string, reportId: string): Promise<DashboardInfo> {
        return Promise.resolve(this.dashboard);
    }

    getTestSuite(projectId: string, reportId: string): Promise<DashboardInfo> {
        return Promise.resolve(this.dashboard);
    }

    getTestSuites(projectId: string): Promise<TestSuiteInfo[]> {
        return [{id: "test_suite1", timestamp: new Date(Date.now())}];
    }
}