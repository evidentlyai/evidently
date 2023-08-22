import React from 'react';
import {Button, Grid, Link, Table, TableBody, TableCell, TableHead, TableRow} from "@material-ui/core";

import {Link as RouterLink} from 'react-router-dom';
import ApiContext from "../lib/contexts/ApiContext";
import LoadableView from "../lib/components/LoadableVIew";
import {ReportInfo} from "../lib/api/Api";
import {DownloadButton} from "./DownloadButton";
import {TextWithCopyIcon} from "./TextWithCopyIcon";
import {formatDate} from "../Utils/Datetime";


const ReportList = (props: { projectId: string, reports: ReportInfo[] }) => {
    return <>
        {/*<form>*/}
        {/*    <input*/}
        {/*        id="contained-button-file"*/}
        {/*        style={{display: "none"}}*/}
        {/*        multiple*/}
        {/*        type="file"*/}
        {/*    />*/}
        {/*    <label htmlFor="contained-button-file">*/}
        {/*        <Button variant="contained" color="primary" component="span">*/}
        {/*            Upload*/}
        {/*        </Button>*/}
        {/*    </label>*/}
        {/*</form>*/}
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>
                        Report ID
                    </TableCell>
                    <TableCell>
                        Timestamp
                    </TableCell>
                    <TableCell>
                        Actions
                    </TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
            {props.reports.map(report => <TableRow id={report.id}>
                <TableCell>
                    <TextWithCopyIcon showText={report.id} copyText={report.id}/>
                </TableCell>
                <TableCell>
                    {formatDate(new Date(Date.parse(report.timestamp)))}
                </TableCell>
                <TableCell>
                    <Link component={RouterLink}
                          to={`/projects/${props.projectId}/reports/${report.id}`}><Button>View</Button></Link>
                    <DownloadButton downloadLink={`/api/projects/${props.projectId}/${report.id}/download`}/>
                </TableCell>
            </TableRow>)}
            </TableBody>
        </Table>
    </>
}

export function Reports(props: { projectId: string }) {
    let {projectId} = props;
    return <>
        <Grid container>
            <Grid item xs={12}>
                <ApiContext.Consumer>
                    {api =>
                        <LoadableView func={() => api.Api.getReports(projectId)}>
                            {reports => <ReportList projectId={projectId} reports={reports}/>}
                        </LoadableView>}
                </ApiContext.Consumer>
            </Grid>
        </Grid>
    </>
}