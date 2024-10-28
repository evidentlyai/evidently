import type React from 'react'

import { Box } from '@mui/material'

import { ResponsiveScatterPlot } from '@nivo/scatterplot'

import type { BigTableDataRow, LineGraphOptions } from '~/api'
import { useNivoTheme } from '~/hooks/theme'

interface ScatterGraphColumnProps extends LineGraphOptions {
  data: BigTableDataRow
}

const _ScatterGraphColumn: React.FunctionComponent<ScatterGraphColumnProps> = (props) => {
  const theme = useNivoTheme()
  return (
    <Box sx={{ maxWidth: 200, height: 50 }}>
      <ResponsiveScatterPlot
        data={[
          {
            id: '1',
            data: props.data[props.xField].map(
              (
                // biome-ignore lint: <explanation>
                val: any,
                idx: number
              ) => ({
                x: val,
                y: props.data[props.yField][idx]
              })
            )
          }
        ]}
        theme={theme}
        margin={{ top: 3, right: 3, bottom: 3, left: 3 }}
        xScale={{ type: 'linear', min: 0, max: 1000 }}
        nodeSize={4}
        colors={[props.color]}
        useMesh={false}
        axisTop={null}
        axisRight={null}
        enableGridX={false}
        enableGridY={false}
      />
    </Box>
  )
}

export const ScatterGraphColumn = _ScatterGraphColumn
