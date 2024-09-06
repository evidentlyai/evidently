import MaterialTable, { type Column, type Options } from '@material-table/core'
import WarningIcon from '@mui/icons-material/Warning'
import { Box, Popover, Typography } from '@mui/material'
import React, { type ReactNode, useState } from 'react'

import type {
  BigTableDataRow,
  BigTableWidgetParams,
  ColumnDefinition,
  HistogramGraphOptions,
  LineGraphOptions,
  ScatterGraphOptions,
  WidgetSize
} from '~/api'

import { BigTableDetails } from './BigTableDetails'
import { GraphDetails } from './GraphDetails'
import { HistogramGraphColumn } from './HistogramGraphColumn'
import { LineGraphColumn } from './LineGraphColumn'
import { ScatterGraphColumn } from './ScatterGraphColumn'

interface BigTableWidgetProps extends BigTableWidgetParams {
  widgetSize: WidgetSize
}

// const useStyles = (theme: Theme) =>
//   createStyles({
//     graph: {
//       maxWidth: 200,
//       height: 50
//     },
//     alert: {
//       width: 50
//     },
//     popup: {
//       padding: theme.spacing(1)
//     }
//   })

const GraphMapping = new Map<
  string,
  (def: ColumnDefinition, row: BigTableDataRow) => React.ReactNode
>([
  [
    'line',
    (def, row) =>
      row[def.field] ? (
        <LineGraphColumn
          xField={(def.options as LineGraphOptions).xField}
          yField={(def.options as LineGraphOptions).yField}
          color={(def.options as LineGraphOptions).color}
          data={row[def.field]}
        />
      ) : (
        <div />
      )
  ],
  [
    'scatter',
    (def, row) =>
      row[def.field] ? (
        <ScatterGraphColumn
          xField={(def.options as ScatterGraphOptions).xField}
          yField={(def.options as ScatterGraphOptions).yField}
          color={(def.options as LineGraphOptions).color}
          data={row[def.field]}
        />
      ) : (
        <div />
      )
  ],
  [
    'histogram',
    (def, row) =>
      row[def.field] ? (
        <HistogramGraphColumn
          xField={(def.options as HistogramGraphOptions).xField}
          yField={(def.options as HistogramGraphOptions).yField}
          color={(def.options as LineGraphOptions).color}
          data={row[def.field]}
        />
      ) : (
        <div />
      )
  ]
])

const GenerateColumns = (columns: ColumnDefinition[]): Column<ColumnDefinition>[] =>
  columns
    .map((def) => ({ def: def, gen: GraphMapping.get(def.type ?? 'string') }))
    .map(({ def, gen }) =>
      gen
        ? { ...def, type: undefined, render: (row: BigTableDataRow) => gen(def, row) }
        : { ...def, sorting: true, defaultSort: def.sort, type: 'string' }
    )

interface InsightAlertProps {
  longText: ReactNode
}

type InsightAlertState = { open: boolean; anchorEl?: EventTarget & HTMLElement }
const InsightAlert: React.FunctionComponent<InsightAlertProps> = (props) => {
  const [state, setState] = useState<InsightAlertState>({ open: false, anchorEl: undefined })
  return (
    <Box
      sx={{ width: 50 }}
      onClick={(event) => setState((s) => ({ open: !s.open, anchorEl: event.currentTarget }))}
    >
      <WarningIcon />
      <Popover
        open={state.open}
        anchorEl={state.anchorEl}
        anchorOrigin={{ horizontal: 'left', vertical: 'bottom' }}
      >
        <Typography p={1}>{props.longText}</Typography>
      </Popover>
    </Box>
  )
}

const BigTableWidgetContent: React.FunctionComponent<BigTableWidgetProps> = (props) => {
  const { columns, data } = props

  // biome-ignore lint: <explanation>
  const options: Options<any> = {
    search: true,
    showTitle: false,
    pageSize: props.rowsPerPage ?? 5,
    detailPanelColumnStyle: { minWidth: 42 },
    emptyRowsWhenPaging: false
  }

  return (
    <React.Fragment>
      <MaterialTable<BigTableDataRow>
        columns={
          props.showInfoColumn ?? false
            ? [
                ...GenerateColumns(columns),
                {
                  title: 'Info',
                  render: (row) => (
                    <React.Fragment>
                      {row.details?.insights ? (
                        <InsightAlert
                          longText={`${row.details?.insights[0].title}: ${row.details?.insights[0].text}`}
                        />
                      ) : (
                        <div />
                      )}
                    </React.Fragment>
                  ),
                  width: 50
                }
              ]
            : [...GenerateColumns(columns)]
        }
        data={data}
        detailPanel={({ rowData }) =>
          rowData.graphId ? (
            <GraphDetails graphId={rowData.graphId} widgetSize={props.widgetSize} />
          ) : rowData.details ? (
            <BigTableDetails details={rowData.details} widgetSize={props.widgetSize} />
          ) : null
        }
        options={options}
      />
    </React.Fragment>
  )
}

export default BigTableWidgetContent
