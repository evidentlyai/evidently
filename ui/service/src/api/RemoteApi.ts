import {
    AdditionalGraphInfo,
    Api,
    DashboardInfo,
    ProjectInfo,
    ReportInfo,
    TestSuiteInfo,
    WidgetInfo
} from "../lib/api/Api";

export default class RemoteApi implements Api {
    private endpoint: string;
    public constructor(endpoint: string) {
        this.endpoint = endpoint;
    }
    async getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${graphId}`);
        if (resp.ok) {
            return (await resp.json() as AdditionalGraphInfo);
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${widgetId}`);
        if (resp.ok) {
            return (await resp.json() as WidgetInfo);
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`);
        if (resp.ok) {
            return (await resp.json() as DashboardInfo);
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getProjects(): Promise<ProjectInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects`);
        console.log(resp);
        if (resp.ok) {
            let projects = await resp.json() as ProjectInfo[];
            console.log(projects);
            return projects;
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getProjectDashboard(projectId: string): Promise<DashboardInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/dashboard`);
        console.log(resp);
        if (resp.ok) {
            return (await resp.json() as DashboardInfo);
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getReports(projectId: string): Promise<ReportInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/reports`);
        if (resp.ok) {
            return (await resp.json() as ReportInfo[]);
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getTestSuites(projectId: string): Promise<TestSuiteInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/test_suites`);
        if (resp.ok) {
            return (await resp.json() as TestSuiteInfo[]);
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }
}