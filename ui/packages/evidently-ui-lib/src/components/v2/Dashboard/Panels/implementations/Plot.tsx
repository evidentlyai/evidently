import { Stack } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import {
  ChartDataProvider,
  ChartsAxisHighlight,
  ChartsGrid,
  ChartsLegend,
  ChartsSurface,
  ChartsTooltip,
  ChartsXAxis,
  ChartsYAxis,
  LinePlot,
  MarkPlot,
  blueberryTwilightPalette,
  useDrawingArea,
  useXAxis
} from '@mui/x-charts'
import { BarPlot } from '@mui/x-charts'
import type { UseChartSeriesParameters } from '@mui/x-charts/internals'

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
import { clamp } from 'evidently-ui-lib/utils/index'
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
}>

type SeriesType = Exclude<UseChartSeriesParameters['series'], undefined>[number]

const HighlightSelectionCustom = ({ onSelect }: { onSelect: (index: number) => void }) => {
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
        style={{ cursor: 'pointer' }}
        onClick={(e) => {
          // @ts-ignore
          const rect = e.target.getBoundingClientRect() // TODO: Fix this hack to track clicks

          const index = Math.floor((e.clientX - rect.x) / gapWidth)

          const newIndex = clamp({ value: index, min: 0, max: xAxis.tickNumber - 1 })

          onSelect(newIndex)
        }}
      />
    </>
  )
}

const Highlight = ({ index }: { index: number }) => {
  const { left, top, width, height } = useDrawingArea()
  const xAxis = useXAxis()
  const theme = useTheme()

  const gapWidth = width / xAxis.tickNumber

  return (
    <rect
      x={left + gapWidth * index}
      y={top}
      width={gapWidth}
      height={height}
      fill={theme.palette.text.primary}
      shapeRendering={'crispEdges'}
      pointerEvents={'none'}
      opacity={0.1}
    />
  )
}

export const PlotDashboardPanel = ({
  data,
  type,
  title,
  description,
  height = 350,
  labels,
  isStacked
}: PlotPanelProps) => {
  const viewParams = useDashboardViewParams()
  const OnClickComponent = viewParams?.OnClickedPointComponent

  const [highlightInfo, setHighlightInfo] = useState<{ index: number } | null>(null)

  const series: SeriesType[] = data.series.map(
    ({ values: data, params, metric_type, filter_index }) => {
      const metricName = metric_type.split(':').at(-1)
      const defaultLabel = [metricName, jsonToKeyValueRowString(params)].filter(Boolean).join('\n')

      const customLabel = formatLabelWithParams({ label: labels?.[filter_index] ?? '', params })

      const common = {
        label: customLabel || defaultLabel,
        stack: isStacked ? 'total' : undefined,
        labelMarkType: 'square' as const
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

  const selectedSnapshotId = highlightInfo && data.sources[highlightInfo.index].snapshot_id

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
          <ChartDataProvider series={series} xAxis={xAxis} colors={blueberryTwilightPalette}>
            <Stack direction={'row'} gap={1} height={'100%'}>
              <ChartsSurface>
                <BarPlot />
                <LinePlot />

                <ChartsXAxis label='Timestamps' position='bottom' />
                <ChartsYAxis position='left' />

                <ChartsTooltip trigger={'axis'} />
                <ChartsGrid horizontal />
                <MarkPlot />

                <ChartsAxisHighlight x={'band'} />

                {OnClickComponent && (
                  <>
                    <HighlightSelectionCustom onSelect={(index) => setHighlightInfo({ index })} />
                    {highlightInfo && <Highlight {...highlightInfo} />}
                  </>
                )}
              </ChartsSurface>

              <Box maxWidth={300}>
                <ChartsLegend
                  slotProps={{
                    legend: {
                      direction: 'vertical',
                      sx: {
                        fontSize: 15,
                        overflow: 'scroll',
                        flexWrap: 'nowrap',
                        height: '85%',
                        whiteSpace: 'pre'
                      }
                    }
                  }}
                />
              </Box>
            </Stack>
          </ChartDataProvider>

          {OnClickComponent && selectedSnapshotId && (
            <Box position={'relative'}>
              <Stack position={'absolute'} top={-20} right={-15}>
                <OnClickComponent snapshotId={selectedSnapshotId} />
              </Stack>
            </Box>
          )}
        </Box>
      </CardContent>
    </Card>
  )
}
