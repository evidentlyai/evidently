import React from "react";

import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

import {createStyles, Theme, WithStyles, withStyles} from "@material-ui/core/styles";

import {CounterInfo} from "../api/Api";

interface CounterWidgetProps {
    counters: CounterInfo[];
}

const styles = (theme: Theme) => createStyles({
    base: {
        height: "100%"
    },
    value: {
        fontSize: 36,
        textAlign: "center"
    },
    label: {
        fontSize: 24,
        textAlign: "center"
    },

});

const CounterItem: React.FunctionComponent<CounterInfo & WithStyles> = (props) => (
    <div>
        <Typography className={props.classes.value}>{props.value}</Typography>
        <Typography className={props.classes.label}>{props.label}</Typography>
    </div>
)

const CounterWidgetContent: React.FunctionComponent<CounterWidgetProps & WithStyles> = (props) =>
    (<React.Fragment>{
        props.counters.length === 1
            ? <CounterItem {...props.counters[0]} classes={props.classes}/>
            : <Grid container spacing={1} direction="row" alignItems="center">
                {
                    props.counters.map((counter, idx) =>
                    <Grid item xs key={idx} component={Box} className={props.classes.base}>
                        <Paper><CounterItem classes={props.classes} {...counter} /></Paper>
                    </Grid>)
                }
            </Grid>
    }</React.Fragment>)

export default withStyles(styles)(CounterWidgetContent);