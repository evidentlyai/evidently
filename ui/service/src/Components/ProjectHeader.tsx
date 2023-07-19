import React from 'react';
import {Grid, Typography} from "@material-ui/core";


export function ProjectHeader(props: {projectName: string, description: string}) {
    return <>
        <Grid container>
            <Grid item xs={12}>
                <Typography variant={"h3"}>{props.projectName}</Typography>
            </Grid>
            <Grid item xs={12} style={{paddingTop: "10px"}}>
                <Typography>{props.description}</Typography>
            </Grid>
        </Grid>
    </>
}