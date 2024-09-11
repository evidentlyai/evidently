import type React from 'react'

import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material'

import type { TableWidgetParams } from '~/api'

const TableWidgetContent: React.FunctionComponent<TableWidgetParams> = (props) => (
  <TableContainer>
    <Table sx={{ minWidth: 650 }} size='small' aria-label='a dense table'>
      <TableHead>
        <TableRow>
          <TableCell key={-1}>{props.header[0]}</TableCell>
          {props.header.slice(1).map((val) => (
            <TableCell key={val} align='right'>
              {val}
            </TableCell>
          ))}
        </TableRow>
      </TableHead>
      <TableBody>
        {props.data.map((row) => (
          <TableRow key={row[0]}>
            <TableCell key={-1} component='th' scope='row'>
              {row[0]}
            </TableCell>
            {row.slice(1).map((val) => (
              <TableCell key={val} align='right'>
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
