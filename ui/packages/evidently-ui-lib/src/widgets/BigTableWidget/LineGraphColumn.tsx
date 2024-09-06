import { Box } from '@mui/material'
import type React from 'react'

// import {WithStyles, WithTheme} from "@material-ui/core/styles";
import { ResponsiveLineCanvas } from '@nivo/line'

import type { BigTableDataRow, LineGraphOptions } from '~/api'
// import withTheme from "@material-ui/core/styles/withTheme";

interface LineGraphColumnProps extends LineGraphOptions {
  data: BigTableDataRow
}

const _LineGraphColumn: React.FunctionComponent<LineGraphColumnProps> = (props) => {
  return (
    <Box sx={{ maxWidth: 200, height: 50 }}>
      <ResponsiveLineCanvas
        data={[
          {
            id: '1',
            // biome-ignore lint: FIX IT
            data: props.data[props.xField].map((val: any, idx: number) => ({
              x: val,
              y: props.data[props.yField][idx]
            }))
          }
        ]}
        margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
        xScale={{ type: 'linear', min: 0, max: 25 }}
        axisTop={null}
        colors={[props.color]}
        axisRight={null}
        enableGridX={false}
        enableGridY={false}
      />
    </Box>
  )
}

export const LineGraphColumn = _LineGraphColumn
