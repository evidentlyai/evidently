import React from "react";

import Box from "@material-ui/core/Box";
import LinearProgress from "@material-ui/core/LinearProgress";
import Typography from "@material-ui/core/Typography";

import {PercentWidgetParams} from "../api/Api";


const ProgressWidgetContent: React.FunctionComponent<PercentWidgetParams> =
    (props) =>
        (<div>
            <Box display="flex" alignItems="center">
                <Box width="100%" mr={1}>
                    <LinearProgress variant="determinate" value={(props.value / props.maxValue) * 100}/>
                </Box>
                <Box minWidth={35}>
                    <Typography variant="body2" color="textSecondary">{`${Math.round(
                        (props.value / props.maxValue) * 100,
                    )}%`}</Typography>
                </Box>
            </Box>
            <Box width="100%">
                <Typography variant="body2" color="textSecondary">{props.details ?? ""}</Typography>
            </Box>
        </div>);


export default ProgressWidgetContent;
