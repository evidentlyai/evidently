import React from 'react';

import {Link as RouterLink} from 'react-router-dom';
import {Grid, Link, Paper, Typography} from "@material-ui/core";
import ApiContext from "../lib/contexts/ApiContext";
import LoadableView from "../lib/components/LoadableVIew";


export const ProjectList = (props: {}) => {

    return <>
        <Typography variant={"h5"}>Project List</Typography>
        <Grid container direction={"column"} justifyContent={"center"} alignItems={"stretch"}>
            <ApiContext.Consumer>
                {api => {
                    return <LoadableView func={() => api.Api.getProjects()}>
                        {
                            params => {
                                return params.map(proj => <Paper style={{margin: "5px", padding: "10px"}}>
                                    <Grid item>
                                        <Link component={RouterLink} to={`/projects/${proj.id}`}>
                                            <Typography variant={"h6"}>{proj.name}</Typography></Link>
                                    </Grid>
                                    <Grid item>
                                        {proj.description}
                                    </Grid>
                                </Paper>)
                        }}
                    </LoadableView>;
                }}
            </ApiContext.Consumer>
        </Grid>
    </>
}