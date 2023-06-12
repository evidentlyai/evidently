import React from 'react';
import {
    Breadcrumbs,
    Grid,
    Link,
    Paper
} from "@material-ui/core";
import {Link as RouterLink, useParams} from "react-router-dom";
import {ProjectHeader} from "./ProjectHeader";
import {ProjectData} from "./ProjectData"
import {ServiceHeader} from "./ServiceHeader";


export async function loader(params: {projectId: string}) {
  return params;
}

export function ServiceApp(props: {}) {
    let { projectId, reportId } = useParams();
    console.log(projectId);
    return <>
        <ServiceHeader />
        <Paper style={{marginTop: "20px", marginLeft: "10px", marginRight: "10px", padding: "10px"}}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Breadcrumbs aria-label="breadcrumb">
                        <Link component={RouterLink} color="inherit" to="/">
                            Home
                        </Link>
                        <Link component={RouterLink} color="inherit" to="/project1">
                            Project #1
                        </Link>
                    </Breadcrumbs>
                </Grid>
                <Grid item xs={12}>
                    <ProjectHeader projectName={"Project #1"}
                                   description={"This Project does not have any description yet. But we hope you still remember what is this all about"}/>
                </Grid>
                <Grid item xs={12}>
                    <ProjectData />
                </Grid>
                <Grid item xs={12}>
                </Grid>
            </Grid>
        </Paper>
    </>
}