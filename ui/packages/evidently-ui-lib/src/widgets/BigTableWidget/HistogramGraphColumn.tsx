import { Box } from '@mui/material'
import type React from 'react'

// import {WithStyles, WithTheme} from "@material-ui/core/styles";

import { ResponsiveBarCanvas } from '@nivo/bar'

import type { BigTableDataRow, LineGraphOptions } from '~/api'

interface HistogramGraphColumnProps extends LineGraphOptions {
  data: BigTableDataRow
}

const _HistogramGraphColumn: React.FunctionComponent<HistogramGraphColumnProps> = (props) => {
  return (
    <Box sx={{ maxWidth: 200, height: 50 }}>
      <ResponsiveBarCanvas
        data={props.data[props.xField].map(
          (
            // biome-ignore lint: <explanation>
            v: any,
            idx: number
          ) => ({
            id: v,
            x: props.data[props.yField][idx]
          })
        )}
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
