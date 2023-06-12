import React from "react";

import {Breadcrumbs, Grid, Link} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";


export const ReportsHeader = (props: {projectId: string, reportId?: string}) => {
    return <>
        <Grid item xs={12}>
                <Breadcrumbs aria-label="breadcrumb">
                    <Link component={RouterLink} color="inherit" to={`/projects/${props.projectId}/reports`}>
                        Reports
                    </Link>
                    {props.reportId ? <Link component={RouterLink} color="inherit" to={`/projects/${props.projectId}/reports/${props.reportId}`}>
                        {props.reportId}
                    </Link> : null }
                </Breadcrumbs>
            </Grid>
        </>
};