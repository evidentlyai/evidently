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

import type { RichDataParams } from '~/api'

import Plot, { darkPlotlyLayoutTemplate } from '~/components/Plot'
import { useThemeMode } from '~/hooks/theme'
import { BigTableDetails } from './BigTableWidget/BigTableDetails'

const RichDataWidget: React.FunctionComponent<RichDataParams & { widgetSize: number }> = (
  props
) => {
  const [details, setDetails] = useState<boolean>(false)
  const mode = useThemeMode()

  const tOverride =
    mode === 'dark'
      ? {
          template: {
            ...darkPlotlyLayoutTemplate,
            layout: {
              ...darkPlotlyLayoutTemplate.layout,
              colorway:
                props.graph?.layout.template?.layout?.colorway ||
                darkPlotlyLayoutTemplate.layout?.colorway
            }
          }
        }
      : undefined

  return (
    <React.Fragment>
      <Grid container spacing={2} justifyContent='center' alignItems='center'>
        <Grid size={{ xs: 2 }}>
          <Typography variant={'h5'}>{props.header}</Typography>
          <Typography variant={'subtitle1'}>{props.description}</Typography>
        </Grid>
        <Grid size={{ xs: props.graph === undefined ? 10 : 5 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell />
                {props.metricsValuesHeaders.map((header) => (
                  // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                  <TableCell>{header}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {props.metrics.map((metric) => (
                // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                <TableRow>
                  <TableCell>{metric.label}</TableCell>
                  {metric.values.map((value) => (
                    // biome-ignore lint/correctness/useJsxKeyInIterable: not reordered
                    <TableCell>{value}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Grid>
        {props.graph === undefined ? (
          <></>
        ) : (
          <Grid size={{ xs: 5 }}>
            <Plot
              data={props.graph.data}
              layout={{
                ...props.graph.layout,
                ...tOverride,
                title: undefined
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
            <Grid size={{ xs: 12 }}>
              <Button
                variant='outlined'
                startIcon={details ? <ExpandLessSharpIcon /> : <ExpandMoreSharpIcon />}
                onClick={() => setDetails((prevState) => !prevState)}
              >
                Details
              </Button>
            </Grid>
            <Grid size={{ xs: 12 }}>
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
