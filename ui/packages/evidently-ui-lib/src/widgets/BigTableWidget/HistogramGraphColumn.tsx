import { Box } from '@mui/material'
import type React from 'react'

import { ResponsiveBarCanvas } from '@nivo/bar'

import type { BigTableDataRow, LineGraphOptions } from '~/api'
import { useNivoTheme } from '~/hooks/theme'

interface HistogramGraphColumnProps extends LineGraphOptions {
  data: BigTableDataRow
}

const _HistogramGraphColumn: React.FunctionComponent<HistogramGraphColumnProps> = (props) => {
  const theme = useNivoTheme()
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
        theme={theme}
        margin={{ top: 3, right: 3, bottom: 3, left: 3 }}
        indexBy={'id'}
        keys={['x']}
        colors={[props.color]}
        axisTop={null}
        axisRight={null}
        enableGridX={false}
        enableGridY={false}
        tooltip={({ id, value }) => (
          <div
            style={{
              background: 'rgba(30, 30, 30, 0.95)',
              color: '#fff',
              padding: '6px 10px',
              borderRadius: '4px',
              fontSize: '12px',
              boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
            }}
          >
            <div>
              <strong>Value:</strong> {typeof id === 'number' ? id.toFixed(4) : id}
            </div>
            <div>
              <strong>Percent:</strong> {typeof value === 'number' ? value.toFixed(2) : value}%
            </div>
          </div>
        )}
      />
    </Box>
  )
}

export const HistogramGraphColumn = _HistogramGraphColumn