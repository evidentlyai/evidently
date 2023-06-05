import React, {ReactNode} from "react";

import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";

import {createStyles, WithStyles, Theme, withStyles} from "@material-ui/core/styles";

import AlertBlock from "./AlertBlock";
import {WidgetInfo} from "../api/Api";
import InsightBlock from "./InsightBlock";
import AlertStatBlock from "./AlertStatBlock";


/***
 * base part of widget to control:
 *  - layouts
 *  - colors
 */

export interface WidgetProps {
    size: 1 | 3 | 6 | 12,
    alertPosition?: "row" | "column",
    children: WidgetInfo & { content: ReactNode; }
}

const styles = (theme: Theme) => createStyles({
    widget: {
        padding: theme.spacing(.5),
    },
    widgetInner: {
        height: "100%",
    },
    cardContentOverride: {
        padding: "9px",
    },
    alertArea: {
    },
    customPopup: {
        paddingRight: theme.spacing(1),
    }
})

interface sizes {
    xs: 1 | 3 | 6 | 12,
    sm: 1 | 3 | 6 | 12,
    md: 1 | 3 | 6 | 12,
    lg: 1 | 3 | 6 | 12,
}

function Sizes(size: number): sizes {
    if (size === 12) {
        return {
            xs: 12,
            sm: 12,
            md: 12,
            lg: 12,
        }
    }
    if (size === 6) {
        return {
            xs: 12,
            sm: 12,
            md: 6,
            lg: 6,
        }
    }
    if (size === 3) {
        return {
            xs: 12,
            sm: 6,
            md: 3,
            lg: 3,
        }
    }
    return {
        xs: 6,
        sm: 3,
        md: 1,
        lg: 1,
    }
}


class Widget extends React.Component<WidgetProps & WithStyles, {}> {
    render() {
        const {title, details, content, alerts, alertStats, insights} = this.props.children;
        const alertsPosition = this.props.children.alertsPosition ?? "row";
        const {size, classes} = this.props;
        const isAlertsExists = alerts === undefined ? false : alerts.length > 0;
        const isInsightsExists = insights === undefined ? false : insights.length > 0;
        return <Grid item
                     {...Sizes(size)}
                     className={classes.widget}>
            <Card className={classes.widgetInner} square elevation={2}>
                <CardContent className={classes.cardContentOverride}>
                    <Grid container spacing={1} direction={"column"}>
                        {alertsPosition === "row" ?
                            <Grid container spacing={1}
                                  item>
                                <Grid item
                                      xs={isAlertsExists && alertsPosition === "row" ? 9 : 12}
                                >
                                    {title ? <Typography variant={"h5"}>{title}</Typography> : <div/>}
                                    <div>{content}</div>
                                    {details ? <Typography variant={"subtitle1"}>{details}</Typography> : <div/>}
                                </Grid>
                                {isAlertsExists
                                    ?
                                    <Grid container spacing={1}
                                          direction={"column"}
                                          justify={"center"} item xs={3} className={classes.alertArea}>
                                        {alerts ? <React.Fragment>
                                                {alertStats
                                                    ? <Grid item>
                                                        <AlertStatBlock alertStats={alertStats} classes={classes}/>
                                                    </Grid>
                                                    : <div/>}
                                                {alerts.map(alert => <Grid item><AlertBlock data={alert}/></Grid>)}
                                            </React.Fragment> :
                                            <div/>
                                        }</Grid>
                                    : <div/>}
                            </Grid>
                            : <React.Fragment>
                                <Grid item>
                                    {title ? <Typography variant={"h5"}>{title}</Typography> : <div/>}
                                    <div>{content}</div>
                                    {details ? <Typography variant={"subtitle1"}>{details}</Typography> : <div/>}
                                </Grid>
                                {isAlertsExists
                                    ? <Grid item xs>
                                        <Grid container direction={"row"} spacing={1}>
                                            {alerts ? <React.Fragment>
                                                    {alertStats
                                                        ? <Grid item xs>
                                                            <AlertStatBlock alertStats={alertStats} classes={classes}/>
                                                        </Grid>
                                                        : <div/>}
                                                    {alerts.map(alert => <Grid item xs><AlertBlock
                                                        data={alert}/></Grid>)}
                                                </React.Fragment> :
                                                <div/>}
                                        </Grid>
                                    </Grid>
                                    : <div/>}</React.Fragment>}
                        {isInsightsExists
                            ? insights!.map(insight =>
                                <Grid item xs sm md>
                                    <InsightBlock data={insight}/>
                                </Grid>)
                            : <div/>}
                    </Grid>
                </CardContent>
            </Card>
        </Grid>;
    }
}

export default withStyles(styles)(Widget);