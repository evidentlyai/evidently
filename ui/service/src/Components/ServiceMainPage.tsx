import React from "react";
import {ServiceHeader} from "./ServiceHeader";
import {Breadcrumbs, Grid, Link, Paper} from "@material-ui/core";
import {Link as RouterLink} from "react-router-dom";
import {ProjectHeader} from "./ProjectHeader";
import {ProjectData} from "./ProjectData";
import LoadableView from "../lib/components/LoadableVIew";
import ApiContext from "../lib/contexts/ApiContext";
import {ProjectContext} from "../Contexts/ProjectContext";


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
            {projectId === undefined ? <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Breadcrumbs aria-label="breadcrumb">
                                    <Link component={RouterLink} color="inherit" to="/">
                                        Home
                                    </Link>
                                </Breadcrumbs>
                            </Grid>
                            <Grid item xs={12}>
                                {children}
                            </Grid>
                        </Grid> :
                <ApiContext.Consumer>{
                    api => <LoadableView func={() => api.Api.getProjectInfo(projectId!)}>{
                        project => <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Breadcrumbs aria-label="breadcrumb">
                                    <Link component={RouterLink} color="inherit" to="/">
                                        Home
                                    </Link>
                                    {projectId ?
                                        <Link component={RouterLink} color="inherit" to={`/projects/${project.id}`}>
                                            {project.project_name}
                                        </Link> : null}
                                </Breadcrumbs>
                            </Grid>
                            {/*<Grid item xs={12}>*/}
                            {/*    <ProjectHeader projectName={"Project #1"}*/}
                            {/*                   description={"This Project does not have any description yet. But we hope you still remember what is this all about"}/>*/}
                            {/*</Grid>*/}
                            <Grid item xs={12}>
                                <ProjectContext.Provider value={project}>
                                    {children}
                                </ProjectContext.Provider>
                            </Grid>
                        </Grid>}
                    </LoadableView>}
                </ApiContext.Consumer>
            }
        </Paper>
    </>
}