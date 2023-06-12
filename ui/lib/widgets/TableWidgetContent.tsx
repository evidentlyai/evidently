import React from "react";

import Paper from "@material-ui/core/Paper";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";

import {createStyles, Theme, withStyles, WithStyles} from "@material-ui/core/styles";

import {TableWidgetParams} from "../api/Api";

const styles = (theme: Theme) => createStyles({
    table: {
        minWidth: 650,
    },
});

const TableWidgetContent: React.FunctionComponent<TableWidgetParams & WithStyles> =
    (props) =>
    <TableContainer component={Paper}>
        <Table className={props.classes.table} size="small" aria-label="a dense table">
            <TableHead>
                <TableRow>
                    <TableCell key={-1}>{props.header[0]}</TableCell>
                    {props.header.slice(1).map((val, idx) => (
                        <TableCell key={idx} align="right">{val}</TableCell>
                    ))}
                </TableRow>
            </TableHead>
            <TableBody>
                {props.data.map((row) => (
                    <TableRow key={row[0]}>
                        <TableCell key={-1} component="th" scope="row">
                            {row[0]}
                        </TableCell>
                        {row.slice(1).map((val, idx) => (
                            <TableCell key={idx} align="right">{val}</TableCell>
                        ))}
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    </TableContainer>;


export default withStyles(styles)(TableWidgetContent);