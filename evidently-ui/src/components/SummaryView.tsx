import React from "react";

import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Select from "@material-ui/core/Select";
import {createStyles, makeStyles} from "@material-ui/core/styles";

import {DashboardInfo} from "../api/Api";
import {DashboardContent} from "./DashboardContent";

const useStyles = makeStyles((theme) =>
    createStyles({
        root: {
            marginTop: 10,
            flexGrow: 1,
        },
        paper: {
            padding: theme.spacing(2),
            textAlign: 'center',
            color: theme.palette.text.secondary,
        },
        header: {
            display: "flex",
            verticalAlign: "baseline",
        },
        filler: {
            flexGrow: 1,
        },
        headerAction: {
            marginLeft: theme.spacing(1),
        }
    }),
);

interface SummaryViewProps
{
    dashboardInfo: DashboardInfo;
}

const SummaryView: React.FunctionComponent<SummaryViewProps> = (props) => {
    const classes = useStyles();
    console.log(props);
    return (
        <div className={classes.root}>
            <Grid container spacing={3} direction="row" alignItems="stretch">
                <Grid item xs={12} className={classes.header}>
                    <Select
                        label="Age"
                        labelId="time_range_label"
                        value={"recent"}
                        inputProps={{
                            name: 'age',
                            id: 'age-native-simple',
                        }}
                    >
                        <option value={"6m"}>Last 6 months</option>
                        <option value={"3m"}>Last 3 months</option>
                        <option value={"recent"}>Recent data</option>
                    </Select>
                    <div className={classes.filler}/>
                    <Box>
                        <Button className={classes.headerAction} variant={"contained"} color="primary">Edit</Button>
                        <Button className={classes.headerAction} variant={"contained"} color="primary">Export</Button>
                    </Box>
                </Grid>
                <DashboardContent info={props.dashboardInfo}/>
            </Grid>
        </div>
    )
};

export default SummaryView;