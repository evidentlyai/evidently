import React from "react";

import {
    AdditionalGraphInfo,
    Api,
    DashboardInfo,
    ProjectDetails,
    ProjectInfo,
    ReportInfo,
    TestSuiteInfo,
    WidgetInfo,
    VersionInfo
} from "../api/Api";

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

    getProjectDashboard(projectId: string): Promise<DashboardInfo> {
        return Promise.reject("not implemented");
    }

    getReports(projectId: string): Promise<ReportInfo[]> {
        return Promise.reject("not implemented");
    }

    getProjectInfo(projectId: string): Promise<ProjectDetails> {
        return Promise.reject("not implemented");
    }

    getTestSuites(projectId: string): Promise<TestSuiteInfo[]> {
        return Promise.resolve([]);
    }

    getVersion(): Promise<VersionInfo> {
        return Promise.resolve({version: "0.0.0"});
    }

}

const ApiContext = React.createContext<ApiContextState>({Api: new NotImplementedApi()});

export default ApiContext;