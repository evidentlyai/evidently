import React from "react";

import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";

import AlertBlock from "./AlertBlock";
import {AlertStats} from "../api/Api";

interface AlertStatBlockProps
{
    alertStats: AlertStats;
}


const useStyles = makeStyles(theme => ({
    customPopup: {
        paddingRight: theme.spacing(1),
    }
}))

const AlertStatBlock : React.FunctionComponent<AlertStatBlockProps> = (props) => {
    const {alertStats} = props;
    const classes = useStyles();
    return <AlertBlock data={{
        value: `${alertStats.triggered.last_24h}`,
        state: "info",
        text: "alerts in the last 24 hours",
        longText: "alerts triggered in the period / alerts triggered in 24 hours / alerts active "
    }}
                       customPopup={<Typography className={classes.customPopup}>
                           <ul>
                               <li>{alertStats.triggered.period} alerts
                                   triggered in the period
                               </li>
                               <li>{alertStats.triggered.last_24h} alerts
                                   triggered in 24 hours
                               </li>
                               <li>{alertStats.active} total active alerts</li>
                           </ul>
                       </Typography>}
    />
}

export default AlertStatBlock;