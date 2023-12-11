import React from 'react'

import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material'

import { TableWidgetParams } from '~/api'

const TableWidgetContent: React.FunctionComponent<TableWidgetParams> = (props) => (
  <TableContainer component={Paper}>
    <Table sx={{ minWidth: 650 }} size="small" aria-label="a dense table">
      <TableHead>
        <TableRow>
          <TableCell key={-1}>{props.header[0]}</TableCell>
          {props.header.slice(1).map((val, idx) => (
            <TableCell key={idx} align="right">
              {val}
            </TableCell>
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
              <TableCell key={idx} align="right">
                {val}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
)

export default TableWidgetContent
