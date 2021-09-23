import React, {ReactNode, useState} from "react";

import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";
import Popover from "@material-ui/core/Popover";

import {createStyles, Theme, WithStyles, withStyles} from "@material-ui/core/styles";
import {lighten, darken} from "@material-ui/core/styles";

import {MetricAlertParams} from "../api/Api";

interface AlertBlockProps {
    data: MetricAlertParams;
    customPopup?: ReactNode;
}

function getBackgroundColor(theme: Theme) {
    return theme.palette.type === "light"
        ? lighten
        : darken
}

function getColor(theme: Theme) {
    return theme.palette.type === "light"
        ? darken
        : lighten
}

const styles = (theme: Theme) => createStyles({
    metric: {},
    metricText: {},
    text: {
        fontSize: theme.typography.fontSize + 5,
    },
    info: {
        color: getColor(theme)(theme.palette.info.main, 0.6),
        backgroundColor: getBackgroundColor(theme)(theme.palette.info.main, 0.9),
    },
    success: {
        color: getColor(theme)(theme.palette.success.main, 0.6),
        backgroundColor: getBackgroundColor(theme)(theme.palette.success.main, 0.9),
    },
    warning: {
        color: getColor(theme)(theme.palette.warning.main, 0.6),
        backgroundColor: getBackgroundColor(theme)(theme.palette.warning.main, 0.9),
    },
    error: {
        color: getColor(theme)(theme.palette.error.main, 0.6),
        backgroundColor: getBackgroundColor(theme)(theme.palette.error.main, 0.9),
    },
    popup: {
        padding: theme.spacing(1),
    }
})

function getStyleByName(name: "info" | "success" | "warning" | "error", classes: WithStyles) {
    switch (name) {
        case "success":
            return classes.classes.success;
        case "info":
            return classes.classes.info;
        case "warning":
            return classes.classes.warning;
        case "error":
            return classes.classes.error;
    }
}

interface PopoverState {
    open: boolean;
    anchorEl?: EventTarget & HTMLElement;
}

const AlertBlock: React.FunctionComponent<AlertBlockProps & WithStyles> = (props) => {
    const [state, setState] = useState<PopoverState>({open: false});
    return (
        <Paper elevation={0}
               onClick={(event) => setState(s => ({open: !s.open, anchorEl: event.currentTarget}))}
               className={getStyleByName(props.data.state ?? "info", props)}
        >
            <Typography
                align={"center"}
                variant={"h6"}
                component={"div"}
                className={props.classes.metric}>
                {props.data.value}
            </Typography>
            <Typography
                align={"center"}
                variant={"body1"}
                component={"div"}
                className={props.classes.metricText}>
                {props.data.text}
            </Typography>
            <Popover open={state.open}
                     anchorEl={state.anchorEl}
                     anchorOrigin={{horizontal: "left", vertical: "bottom"}}
            >{props.customPopup ??
            <Typography className={props.classes.popup}>{props.data.longText}</Typography>}</Popover>
        </Paper>)
}

export default withStyles(styles)(AlertBlock);