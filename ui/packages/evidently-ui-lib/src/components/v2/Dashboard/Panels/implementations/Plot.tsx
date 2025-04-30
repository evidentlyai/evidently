import { CardActions } from '@mui/material'
import { styled } from '@mui/material/styles'
import { useDrawingArea, useXAxis } from '@mui/x-charts'
import { BarPlot } from '@mui/x-charts/BarChart/BarPlot'
import { ChartsAxisHighlight } from '@mui/x-charts/ChartsAxisHighlight/ChartsAxisHighlight'
import { ChartsGrid } from '@mui/x-charts/ChartsGrid/ChartsGrid'
import { ChartsLegend } from '@mui/x-charts/ChartsLegend/ChartsLegend'
import { ChartsTooltip } from '@mui/x-charts/ChartsTooltip/ChartsTooltip'
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis/ChartsXAxis'
import { ChartsYAxis } from '@mui/x-charts/ChartsYAxis/ChartsYAxis'
import { LinePlot } from '@mui/x-charts/LineChart/LinePlot'
import { MarkPlot } from '@mui/x-charts/LineChart/MarkPlot'
import { ResponsiveChartContainer } from '@mui/x-charts/ResponsiveChartContainer'
import type { SeriesProviderProps } from '@mui/x-charts/context/SeriesProvider'
import dayjs from 'dayjs'
import type { SeriesModel } from 'evidently-ui-lib/api/types/v2'
import {
  Box,
  Card,
  CardContent,
  Divider,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { assertNever } from 'evidently-ui-lib/utils/index'
import { useState } from 'react'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { formatLabelWithParams, jsonToKeyValueRowString } from '~/components/v2/Dashboard/utils'
import { useDashboardViewParams } from '~/contexts/DashboardViewParamsV2'

export type PlotPanelProps = MakePanel<{
  data: SeriesModel
  labels: (string | undefined | null)[]
  type: 'bar' | 'line'
  size: 'full' | 'half'
  isStacked?: boolean
  title?: string
  description?: string
  height?: number
  legendMarginRight?: number
}>

type SeriesType = SeriesProviderProps['series'][number]

const StyledRect = styled('rect')<{ color: 'primary' | 'secondary' }>(({ theme, color }) => ({
  fill: theme.palette.text[color],
  shapeRendering: 'crispEdges',
  pointerEvents: 'none'
}))

const BackgroundSelection = ({
  x,
  onSelect
}: { x?: number; onSelect: (index: number) => void }) => {
  const { left, top, width, height } = useDrawingArea()
  const xAxis = useXAxis()
  const gapWidth = width / xAxis.tickNumber

  return (
    <>
      {/* biome-ignore lint/a11y/useKeyWithClickEvents: No need for key support in this case */}
      <rect
        x={left}
        y={top}
        width={width}
        height={height}
        opacity={0}
        onClick={(e) => {
          // @ts-ignore
          const rec = e.target.getBoundingClientRect() // TODO: Fix this hack to track clicks
          let newIndex = Math.floor((e.clientX - rec.x) / gapWidth)
          newIndex =
            newIndex < 0 ? 0 : newIndex >= xAxis.tickNumber ? xAxis.tickNumber - 1 : newIndex
          onSelect(newIndex)
        }}
      />
      {x && (
        <StyledRect
          x={left + gapWidth * x}
          y={top}
          width={gapWidth}
          height={height}
          color={'primary'}
          opacity={0.1}
        />
      )}
    </>
  )
}

export const PlotDashboardPanel = ({
  data,
  type,
  title,
  description,
  height = 350,
  labels,
  legendMarginRight = 300,
  isStacked
}: PlotPanelProps) => {
  const series: SeriesType[] = data.series.map(
    ({ values: data, params, metric_type, filter_index }) => {
      const metricName = metric_type.split(':').at(-1)
      const defaultLabel = [metricName, jsonToKeyValueRowString(params)].filter(Boolean).join('\n')

      const customLabel = formatLabelWithParams({ label: labels?.[filter_index] ?? '', params })

      const common = {
        label: customLabel || defaultLabel,
        stack: isStacked ? 'total' : undefined
      }

      if (type === 'line') {
        return { type: type, data, ...common } satisfies SeriesType
      }

      if (type === 'bar') {
        return { type: type, data, ...common } satisfies SeriesType
      }

      assertNever(type)
    }
  )

  const xAxis = [
    {
      data: data.sources.map((e) => dayjs(e.timestamp).format('YYYY-MM-DD HH:mm:ss')),
      scaleType: 'band' as const
    }
  ]
  const viewParams = useDashboardViewParams()
  const OnClickComponent = viewParams?.OnClickedPointComponent

  const [highlighted, setHighlighted] = useState<{ series: string | number; index: number } | null>(
    null
  )
  return (
    <Card elevation={0}>
      <CardContent sx={{ px: 0 }}>
        <Box px={3}>
          {title && (
            <Typography variant='h5' fontWeight={500} gutterBottom>
              {title}
            </Typography>
          )}

          {description && (
            <Typography fontWeight={400} gutterBottom>
              {description}
            </Typography>
          )}
        </Box>

        {(title || description) && <Divider sx={{ mb: 2, mt: 1 }} />}
        <Box height={height} px={3}>
          <ResponsiveChartContainer
            series={series}
            xAxis={xAxis}
            margin={{ right: legendMarginRight }}
          >
            <BarPlot />
            <LinePlot />
            <ChartsXAxis label='Timestamps' position='bottom' />
            <ChartsYAxis position='left' />
            <ChartsLegend
              slotProps={{
                legend: {
                  labelStyle: { fontSize: 15 },
                  direction: 'column',
                  position: { vertical: 'top', horizontal: 'right' },
                  markGap: 5,
                  itemGap: 15
                }
              }}
            />
            <ChartsTooltip trigger={'axis'} />
            <ChartsAxisHighlight x={'band'} />
            <ChartsGrid horizontal />
            <MarkPlot />
            <BackgroundSelection
              x={highlighted?.index}
              onSelect={(x) =>
                setHighlighted({
                  index: x,
                  series: ''
                })
              }
            />
          </ResponsiveChartContainer>
        </Box>
      </CardContent>
      {highlighted && OnClickComponent && (
        <CardActions
          sx={{
            justifyContent: 'flex-end'
          }}
        >
          <OnClickComponent snapshotId={data.sources[highlighted.index].snapshot_id} />
        </CardActions>
      )}
    </Card>
  )
}
