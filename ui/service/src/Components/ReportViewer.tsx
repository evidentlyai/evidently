import React from 'react';
import {Grid} from "@material-ui/core";
import {ProjectReport} from "../lib/App";
import {ReportsHeader} from "./ReportsHeader";

export function ReportViewer(props: {projectId: string, reportId: string}) {
    let {projectId, reportId} = props;
    return <>
        <Grid container>
            <ReportsHeader projectId={projectId} reportId={reportId}></ReportsHeader>
            <Grid item xs={12}>
                <ProjectReport projectId={props.projectId!} reportId={props.reportId} />
            </Grid>
        </Grid>
    </>
}