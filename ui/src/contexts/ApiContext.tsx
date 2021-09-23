import React from "react";

import {AdditionalGraphInfo, Api, DashboardInfo, ProjectInfo, WidgetInfo} from "../api/Api";

interface ApiContextState {
    Api: Api;
}

class NotImplementedApi implements Api {
    getAdditionalGraphData(projectId: string, dashboardId: string, graphId: string): Promise<AdditionalGraphInfo> {
        return Promise.reject("not implemented");
    }

    getAdditionalWidgetData(projectId: string, dashboardId: string, widgetId: string): Promise<WidgetInfo> {
        return Promise.reject("not implemented");
    }

    getDashboard(projectId: string, dashboardId: string): Promise<DashboardInfo> {
        return Promise.reject("not implemented");
    }

    getProjects(): Promise<ProjectInfo[]> {
        return Promise.reject("not implemented");
    }

}

const ApiContext = React.createContext<ApiContextState>({Api: new NotImplementedApi()});

export default ApiContext;