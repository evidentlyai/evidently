import React from 'react';
import {Button, Grid, Link, Table, TableCell, TableHead, TableRow} from "@material-ui/core";

import {Link as RouterLink} from 'react-router-dom';
import ApiContext from "../lib/contexts/ApiContext";
import LoadableView from "../lib/components/LoadableVIew";
import {ReportsHeader} from "./ReportsHeader";
import {ReportInfo} from "../lib/api/Api";


const ReportList = (props: { projectId: string, reports: ReportInfo[] }) => {
    return <>
        <form>
            <input
                id="contained-button-file"
                style={{display: "none"}}
                multiple
                type="file"
            />
            <label htmlFor="contained-button-file">
                <Button variant="contained" color="primary" component="span">
                    Upload
                </Button>
            </label>
        </form>
        <Table>
            <TableHead>
                <TableCell>
                    Report ID
                </TableCell>
                <TableCell>
                    Timestamp
                </TableCell>
                <TableCell>
                    Actions
                </TableCell>
            </TableHead>
            {props.reports.map(report => <TableRow>
                <TableCell>
                    {report.id}
                </TableCell>
                <TableCell>
                    {report.timestamp.toString()}
                </TableCell>
                <TableCell>
                    <Link component={RouterLink}
                          to={`/projects/${props.projectId}/test_suites/${report.id}`}><Button>View</Button></Link>
                    <Button disabled={true}>Download</Button>
                </TableCell>
            </TableRow>)}
        </Table>
    </>
}

export function TestSuites(props: { projectId: string }) {
    let {projectId} = props;
    return <>
        <Grid container>
            <ReportsHeader projectId={projectId}/>
            <Grid item xs={12}>
                <ApiContext.Consumer>
                    {api =>
                        <LoadableView func={() => api.Api.getTestSuites(projectId)}>
                            {reports => <ReportList projectId={projectId} reports={reports} />}
                        </LoadableView>}
                </ApiContext.Consumer>
            </Grid>
        </Grid>
    </>
}