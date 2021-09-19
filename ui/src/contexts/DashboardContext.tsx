import React from "react";

import {AdditionalGraphInfo} from "../api/Api";

interface DashboardContextState {
    cachedGraphs: Map<string, AdditionalGraphInfo>;
    getAdditionGraphData: (graphId: string) => Promise<AdditionalGraphInfo>
}


const DashboardContext = React.createContext<DashboardContextState>(CreateDashboardContextState(
    (_) => new Promise((resolve, reject) => reject("default context doesn't contain methods to get data"))
));

export function CreateDashboardContextState(getAdditionGraphData: (graphId: string) => Promise<AdditionalGraphInfo>): DashboardContextState {
    return {
        cachedGraphs: new Map<string, AdditionalGraphInfo>(),
        async getAdditionGraphData(graphId) {
            let cached = this.cachedGraphs.get(graphId);
            if (cached !== undefined) {
                return cached;
            }
            cached = await getAdditionGraphData(graphId);
            this.cachedGraphs.set(graphId, cached);
            return cached;
        }
    }
}

export default DashboardContext;