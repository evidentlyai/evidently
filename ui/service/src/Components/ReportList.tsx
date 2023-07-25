import React from 'react';
import {Button, IconButton, Link, Table, TableCell, TableHead, TableRow} from "@material-ui/core";

import {Link as RouterLink} from 'react-router-dom';
import {ReportInfo} from "../lib/api/Api";


export const ReportList = (props: {projectId: string, reports: ReportInfo[]}) => {
    return <>
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
                    <Link component={RouterLink} to={`/projects/${props.projectId}/reports/${report.id}`}><Button>View</Button></Link>
                    <Button disabled={true}>Download</Button>
                </TableCell>
            </TableRow>)}
        </Table>
    </>
}