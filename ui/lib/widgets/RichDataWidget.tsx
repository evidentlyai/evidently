import React, {useState} from "react";

import {Button, Collapse, Grid, Table, TableBody, TableCell, TableHead, TableRow} from "@material-ui/core";
import {ExpandLessSharp, ExpandMoreSharp} from "@material-ui/icons";
import Typography from "@material-ui/core/Typography";

import {RichDataParams} from "../api/Api";

import Plot from "../components/Plot";
import {BigTableDetails} from "./BigTableWidget/BigTableDetails";

const RichDataWidget: React.FunctionComponent<RichDataParams & { widgetSize: number }> =
    (props) => {
        const [details, setDetails] = useState<boolean>(false)
        return (<React.Fragment>
            <Grid container spacing={2} justifyContent="center" alignItems="center">
                <Grid item xs={2}>
                    <Typography variant={"h5"}>{props.header}</Typography>
                    <Typography variant={"subtitle1"}>{props.description}</Typography>
                </Grid>
                <Grid item xs={props.graph === undefined ? 10: 5}>
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
                {props.graph === undefined ? <></>
                    :
                    <Grid item xs={5}>
                        <Plot data={props.graph.data} layout={{
                            ...props.graph.layout,
                            title: undefined,
                        }}
                              config={{responsive: true}}
                              style={{
                                  width: "100%",
                                  minHeight: 150 + 100 * (1 + (props.widgetSize / 2)),
                                  maxHeight: 250
                              }}
                        />
                    </Grid>
                }
                {props.details === undefined || props.details.parts.length === 0 ? <></> :
                    <>
                        <Grid item xs={12}>
                            <Button variant="outlined" startIcon={details ? <ExpandLessSharp/> : <ExpandMoreSharp/>}
                                    onClick={
                                        () => setDetails(prevState => !prevState)
                                    }
                            >Details</Button>
                        </Grid>
                        <Grid item xs={12}>
                            <Collapse in={details} mountOnEnter={true} unmountOnExit={true}>
                                <BigTableDetails details={props.details} widgetSize={props.widgetSize}/>
                            </Collapse>
                        </Grid>
                    </>
                }
            </Grid>
        </React.Fragment>)
    }
export default RichDataWidget;