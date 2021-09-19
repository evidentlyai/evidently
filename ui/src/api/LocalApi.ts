import {AdditionalGraphInfo, Api, DashboardInfo, ProjectInfo} from "./Api";

export default class LocalApi implements Api {
    private readonly dashboard: DashboardInfo;
    private additionalGraphs: Map<string, AdditionalGraphInfo>;

    constructor(dashboard: DashboardInfo, additionalGraphs: Map<string, AdditionalGraphInfo>) {
        this.dashboard = dashboard;
        this.additionalGraphs = additionalGraphs;
    }

    getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        var graph = this.additionalGraphs.get(graphId);
        return graph ? Promise.resolve(graph) : Promise.reject("No graph found");
    }

    getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        return Promise.resolve(this.dashboard);
    }

    getProjects(): Promise<ProjectInfo[]> {
        return Promise.resolve([]);
    }
}