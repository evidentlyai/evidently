import React, { useState } from 'react'

import {
  Button,
  Collapse,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography
} from '@mui/material'

import ExpandLessSharpIcon from '@mui/icons-material/ExpandLessSharp'
import ExpandMoreSharpIcon from '@mui/icons-material/ExpandMoreSharp'

import { RichDataParams } from '~/api'

import Plot from '~/components/Plot'
import { BigTableDetails } from './BigTableWidget/BigTableDetails'
import { useDashboardViewParams } from '~/contexts/DashboardViewParams'

const RichDataWidget: React.FunctionComponent<RichDataParams & { widgetSize: number }> = (
  props
) => {
  const [details, setDetails] = useState<boolean>(false)
  const viewParams = useDashboardViewParams()
  const isHistogram = props.graph?.data.some(({ type }) => type === 'histogram')
  const isCastXaxisToCategory = viewParams?.isXaxisAsCategorical && !isHistogram

  const xaxisOptionsOverride = isCastXaxisToCategory
    ? ({ type: 'category', categoryorder: 'category ascending' } as const)
    : ({} as const)

  return (
    <React.Fragment>
      <Grid container spacing={2} justifyContent="center" alignItems="center">
        <Grid item xs={2}>
          <Typography variant={'h5'}>{props.header}</Typography>
          <Typography variant={'subtitle1'}>{props.description}</Typography>
        </Grid>
        <Grid item xs={props.graph === undefined ? 10 : 5}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell />
                {props.metricsValuesHeaders.map((header, index) => (
                  <TableCell key={header + index}>{header}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {props.metrics.map((metric, index) => (
                <TableRow key={metric.label + index}>
                  <TableCell>{metric.label}</TableCell>
                  {metric.values.map((value, index) => (
                    <TableCell key={String(value) + index}>{value}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Grid>
        {props.graph === undefined ? (
          <></>
        ) : (
          <Grid item xs={5}>
            <Plot
              data={props.graph.data}
              layout={{
                ...props.graph.layout,
                title: undefined,
                xaxis: { ...props.graph.layout?.xaxis, ...xaxisOptionsOverride }
              }}
              config={{ responsive: true }}
              style={{
                width: '100%',
                minHeight: 150 + 100 * (1 + props.widgetSize / 2),
                maxHeight: 250
              }}
            />
          </Grid>
        )}
        {props.details === undefined || props.details.parts.length === 0 ? (
          <></>
        ) : (
          <>
            <Grid item xs={12}>
              <Button
                variant="outlined"
                startIcon={details ? <ExpandLessSharpIcon /> : <ExpandMoreSharpIcon />}
                onClick={() => setDetails((prevState) => !prevState)}
              >
                Details
              </Button>
            </Grid>
            <Grid item xs={12}>
              <Collapse in={details} mountOnEnter={true} unmountOnExit={true}>
                <BigTableDetails details={props.details} widgetSize={props.widgetSize} />
              </Collapse>
            </Grid>
          </>
        )}
      </Grid>
    </React.Fragment>
  )
}
export default RichDataWidget
