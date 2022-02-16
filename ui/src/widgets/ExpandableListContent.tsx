import {Button, Collapse, Grid, Table, TableBody, TableCell, TableHead, TableRow} from "@material-ui/core";
import React, {useState} from "react";
import Plot from "react-plotly.js";

import {ExpandLessSharp, ExpandMoreSharp} from "@material-ui/icons";

import {ExpandableListWidgetParams} from "../api/Api";
import Typography from "@material-ui/core/Typography";
import {BigTableDetails} from "./BigTableWidget/BigTableDetails";

const ExpandableListContent: React.FunctionComponent<ExpandableListWidgetParams & { widgetSize: number }> =
    (props) => {
        const [details, setDetails] = useState<boolean>(false)
        return (<React.Fragment>
            <Grid container spacing={2} justifyContent="center" alignItems="center">
                <Grid item xs={2}>
                    <Typography variant={"h5"}>{props.header}</Typography>
                    <Typography variant={"subtitle1"}>{props.description}</Typography>
                </Grid>
                <Grid item xs={5}>
                    <Table><TableHead><TableRow>
                        <TableCell/>
                        {props.metricsValuesHeaders.map(header => <TableCell>{header}</TableCell>)}
                    </TableRow></TableHead>
                        <TableBody>
                            {props.metrics.map(metric => <TableRow>
                                <TableCell>{metric.label}</TableCell>
                                {metric.values.map(value => <TableCell>{value}</TableCell>)}
                            </TableRow>)}
                        </TableBody></Table>
                </Grid>
                <Grid item xs={5}>
                    <Plot data={props.graph.data} layout={{
                        ...props.graph.layout,
                        title: undefined,
                    }}
                          config={{responsive: true}}
                          style={{width: "100%", minHeight: 150 + 100 * (1 + (props.widgetSize / 2)), maxHeight: 250}}
                    />
                </Grid>
                <Grid item xs={12}>
                    <Button variant="outlined" startIcon={details ? <ExpandLessSharp/> : <ExpandMoreSharp />} onClick={
                        () => setDetails(prevState => !prevState)
                    }>Details</Button>
                </Grid>
            </Grid>
            <Collapse in={details}>
                <BigTableDetails details={props.details} widgetSize={props.widgetSize}/>
            </Collapse>
        </React.Fragment>)
    }
export default ExpandableListContent;