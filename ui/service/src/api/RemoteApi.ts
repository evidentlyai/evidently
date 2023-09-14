import {
    AdditionalGraphInfo,
    Api,
    DashboardInfo, ProjectDetails,
    ProjectInfo,
    ReportInfo,
    TestSuiteInfo, VersionInfo,
    WidgetInfo
} from "../lib/api/Api";

import {JsonParser} from "../lib/ParseJson"

export default class RemoteApi implements Api {
    private readonly endpoint: string;
    public constructor(endpoint: string) {
        this.endpoint = endpoint;
    }
    async getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${graphId}`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as AdditionalGraphInfo;
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/graphs_data/${widgetId}`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as WidgetInfo;
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/${dashboardId}/data`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as DashboardInfo;
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getProjects(): Promise<ProjectInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects`);
        if (resp.ok) {
            let projects = new JsonParser().parse(await resp.text()) as ProjectInfo[];
            console.log(projects);
            return projects;
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getProjectDashboard(projectId: string, from?: string, to?: string): Promise<DashboardInfo> {
        let query = "";
        if (from !== undefined && from !== "") {
            query = `timestamp_start=${from}`
        }
        if (to !== undefined && to !== "") {
            query = (query === "" ? `${query}&` : "") + `timestamp_end=${to}`;
        }
        if (query != "") {
            query = "?" + query;
        }
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/dashboard${query}`);
        console.log(resp);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as DashboardInfo;
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getReports(projectId: string): Promise<ReportInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/reports`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as ReportInfo[];
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getTestSuites(projectId: string): Promise<TestSuiteInfo[]> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/test_suites`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as TestSuiteInfo[];
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getProjectInfo(projectId: string): Promise<ProjectDetails> {
        const resp = await fetch(`${this.endpoint}/projects/${projectId}/info`);
        if (resp.ok) {
            return new JsonParser().parse(await resp.text()) as ProjectDetails;
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async getVersion(): Promise<VersionInfo> {
        const resp = await fetch(`${this.endpoint}/version`);
        if (resp.ok) {
            return (await resp.json() as VersionInfo);
        }
        else
        {
            throw Error(`${resp.status}, ${resp.statusText}`);
        }
    }

    async editProjectInfo(project: ProjectDetails) {
      const response = await fetch(`${this.endpoint}/projects/${project.id}/info`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(project)
      })
  
      if (!response.ok) {
        throw response
      }
  
      return response
    }
}

export const api = new RemoteApi('/api')