import { Box, Button, Stack, Typography } from '@mui/material'
import type React from 'react'
import { useState } from 'react'

import type { AdditionalGraphInfo } from '~/api'
import Plot, { darkPlotlyLayoutTemplate } from '~/components/Plot'
import { useDashboardViewParams } from '~/contexts/DashboardViewParams'
import { useThemeMode } from '~/hooks/theme'

interface BigGraphWidgetProps extends AdditionalGraphInfo {
  widgetSize: number
}

const BigGraphWidgetContent: React.FunctionComponent<BigGraphWidgetProps> = (props) => {
  const viewParams = useDashboardViewParams()
  const mode = useThemeMode()
  const isHistogram = props.data.some(({ type }) => type === 'histogram')
  const isCastXaxisToCategory = viewParams?.isXaxisAsCategorical && !isHistogram

  const [p, setP] = useState('')

  const tOverride =
    mode === 'dark'
      ? {
          template: {
            ...darkPlotlyLayoutTemplate,
            layout: {
              ...darkPlotlyLayoutTemplate.layout,
              colorway:
                props.layout.template?.layout?.colorway || darkPlotlyLayoutTemplate.layout?.colorway
            }
          }
        }
      : undefined
  const xaxisOptionsOverride = isCastXaxisToCategory
    ? ({ type: 'category', categoryorder: 'category ascending' } as const)
    : undefined

  return (
    <>
      <Box position={'relative'}>
        <Plot
          onClick={(e) => {
            console.log(e.points[0])
            const x = e.points[0].x

            setP(String(x))
          }}
          data={props.data}
          layout={{
            ...props.layout,
            ...tOverride,
            title: undefined,
            xaxis: { ...props.layout?.xaxis, ...xaxisOptionsOverride }
          }}
          config={{ responsive: true }}
          style={{
            width: '100%',
            minHeight: 300 + 100 * (1 + props.widgetSize / 2),
            maxHeight: 400
          }}
        />
        {p && (
          <Box sx={{ position: 'absolute', bottom: 0, right: 0 }}>
            <Stack direction={'row'} alignItems={'center'} gap={2}>
              <Typography variant='caption'>
                <b>Timestamp</b> : {p}
                <br />
              </Typography>

              <Button variant='outlined' size='small'>
                Go to snapshot
              </Button>
            </Stack>
          </Box>
        )}
      </Box>
    </>
  )
}

export default BigGraphWidgetContent
