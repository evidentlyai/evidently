import {AdditionalGraphInfo, Api, DashboardInfo, ProjectInfo, WidgetInfo} from "./Api";

export default class LocalApi implements Api {
    private readonly dashboard: DashboardInfo;
    private additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>;

    constructor(dashboard: DashboardInfo, additionalGraphs: Map<string, AdditionalGraphInfo | WidgetInfo>) {
        this.dashboard = dashboard;
        this.additionalGraphs = additionalGraphs;
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
        return Promise.resolve([]);
    }
}