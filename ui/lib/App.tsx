import React, {useContext, useState} from 'react';
import {createTheme, ThemeProvider} from '@material-ui/core/styles';

import {AdditionalGraphInfo, Api, DashboardInfo} from "./api/Api";
import ApiContext from "./contexts/ApiContext";
import DashboardContext, {CreateDashboardContextState} from "./contexts/DashboardContext";
import LoadableView from "./components/LoadableVIew";
import LocalApi from "./api/LocalApi";
import {DashboardContent} from "./components/DashboardContent";
import {Grid} from "@material-ui/core";


export function Report(props: {params: DashboardInfo}) {
    return <Grid container spacing={3} direction="row" alignItems="stretch">
        <DashboardContent info={props.params}/>
    </Grid>
}

export const ProjectDashboard = (props: {projectId: string, from?: string, to?: string}) => {
    let callback =  (api: Api) => api.getProjectDashboard(props.projectId, props.from, props.to);
    return <>
        <ApiContext.Consumer>
            {api =>
                    <LoadableView func={() => callback(api.Api)}>
                        {
                            params =><><Report params={params} /></>
                        }
                    </LoadableView>
            }
        </ApiContext.Consumer>
    </>
}

export function ProjectReport(props: { projectId: string, reportId: string }) {
    let {projectId, reportId} = props;
    return <>
        <ApiContext.Consumer>
            {api =>
                <DashboardContext.Provider value={CreateDashboardContextState(
                    {
                        getAdditionGraphData: graphId => api.Api!.getAdditionalGraphData(
                            projectId,
                            reportId,
                            graphId
                        ),
                        getAdditionWidgetData: widgetId => api.Api!.getAdditionalWidgetData(
                            projectId,
                            reportId,
                            widgetId
                        ),
                    }
                )}>
                    <LoadableView func={() => api.Api.getDashboard(projectId, reportId)}>
                        {
                            params => <Report params={params} />
                        }
                    </LoadableView>

                </DashboardContext.Provider>
            }
        </ApiContext.Consumer>
    </>
}
