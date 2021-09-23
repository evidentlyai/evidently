import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

import {AdditionalGraphInfo, DashboardInfo} from "./api/Api";


export function drawDashboard(dashboard: DashboardInfo, additionalGraphs: Map<string, AdditionalGraphInfo>, tagId: string) {
    ReactDOM.render(
        <React.StrictMode>
            <App dashboard={dashboard} additionalGraphs={additionalGraphs} />
        </React.StrictMode>,
        document.getElementById(tagId)
    );
}

// @ts-ignore
window.drawDashboard = drawDashboard;

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.unregister();
