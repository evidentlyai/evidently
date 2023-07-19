import React from "react";

import {createStyles, Theme, WithStyles, withStyles} from "@material-ui/core/styles";

import Alert from '@material-ui/lab/Alert';
import AlertTitle from '@material-ui/lab/AlertTitle';

import {InsightsParams} from "../api/Api";

interface InsightBlockProps {
    data: InsightsParams;
}

const styles = (theme: Theme) => createStyles({})


const InsightBlock: React.FunctionComponent<InsightBlockProps & WithStyles> = (props) => {
    return <Alert severity={props.data.severity}>
        <AlertTitle>{props.data.title}</AlertTitle>
        {props.data.text}
    </Alert>;
}

export default withStyles(styles)(InsightBlock);