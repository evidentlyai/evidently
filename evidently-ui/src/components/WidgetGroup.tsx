import React from "react";

import Box from "@material-ui/core/Box";
import Divider from "@material-ui/core/Divider";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";

import {createStyles,Theme,WithStyles,withStyles} from "@material-ui/core/styles";

interface WidgetGroupProps {
    title: string;
}


const useStyles = (theme: Theme) => createStyles({
    base: {
        padding: 10,
    },
    iconTab: {
        display: "flex",
    }
});

const WidgetGroup: React.FunctionComponent<WidgetGroupProps & WithStyles> = (props) =>
    <Grid item xs={12} component={Box}>
        <Typography variant={"h5"}>{props.title}</Typography>
        <Grid container spacing={3} className={props.classes.base}>
            {props.children}
        </Grid>
        <Divider />
    </Grid>

export default withStyles(useStyles)(WidgetGroup);