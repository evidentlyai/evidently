import {AdditionalGraphInfo, Api, DashboardInfo, ProjectInfo, WidgetInfo} from "./Api";

export default class RemoteApi implements Api {
    private endpoint: string;
    public constructor(endpoint: string) {
        this.endpoint = endpoint;
    }
    getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        throw Error("not implement");
    }

    getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo> {
        throw Error("not implement");
    }

    async getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        var resp = await fetch(`${this.endpoint}/${projectId}/${dashboardId}`);
        if (resp.ok) {
            return (await resp.json() as DashboardInfo)
        }
        else {
            throw Error(`${resp.status}, ${resp.statusText}`)
        }
    }

    getProjects(): Promise<ProjectInfo[]> {
        return Promise.resolve([]);
    }
}