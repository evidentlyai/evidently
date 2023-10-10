import React from 'react'
import { Box } from '@mui/material'

// import {WithStyles, WithTheme} from "@material-ui/core/styles";

import { ResponsiveBarCanvas } from '@nivo/bar'

import { BigTableDataRow, LineGraphOptions } from '../../api'

interface HistogramGraphColumnProps extends LineGraphOptions {
  data: BigTableDataRow
}

const _HistogramGraphColumn: React.FunctionComponent<HistogramGraphColumnProps> = (props) => {
  return (
    <Box sx={{ maxWidth: 200, height: 50 }}>
      <ResponsiveBarCanvas
        data={props.data[props.xField].map((v: any, idx: number) => ({
          id: v,
          x: props.data[props.yField][idx]
        }))}
        margin={{ top: 3, right: 3, bottom: 3, left: 3 }}
        indexBy={'id'}
        keys={['x']}
        colors={[props.color]}
        axisTop={null}
        axisRight={null}
        enableGridX={false}
        enableGridY={false}
      />
    </Box>
  )
}

export const HistogramGraphColumn = _HistogramGraphColumn
