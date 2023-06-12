import React from "react";
import {ServiceHeader} from "./ServiceHeader";
import {Breadcrumbs, Grid, Link, Paper} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {ProjectHeader} from "./ProjectHeader";
import {ProjectData} from "./ProjectData";


export interface ServiceMainPageProps {
    children: React.JSX.Element
    projectId?: string
    reportId?: string
}


export function ServiceMainPage(props: ServiceMainPageProps) {
    let {children, projectId} = props;
    return <>
        <ServiceHeader/>
        <Paper style={{marginTop: "20px", marginLeft: "10px", marginRight: "10px", padding: "10px"}}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Breadcrumbs aria-label="breadcrumb">
                        <Link component={RouterLink} color="inherit" to="/">
                            Home
                        </Link>
                        {projectId ? <Link component={RouterLink} color="inherit" to="/project1">
                            Project #1
                        </Link> : null}
                    </Breadcrumbs>
                </Grid>
                {/*<Grid item xs={12}>*/}
                {/*    <ProjectHeader projectName={"Project #1"}*/}
                {/*                   description={"This Project does not have any description yet. But we hope you still remember what is this all about"}/>*/}
                {/*</Grid>*/}
                <Grid item xs={12}>
                    {children}
                </Grid>
                <Grid item xs={12}>
                </Grid>
            </Grid>
        </Paper>
    </>
}