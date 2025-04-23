import { BarPlot } from '@mui/x-charts/BarChart/BarPlot'
import { ChartsAxisHighlight } from '@mui/x-charts/ChartsAxisHighlight/ChartsAxisHighlight'
import { ChartsGrid } from '@mui/x-charts/ChartsGrid/ChartsGrid'
import { ChartsLegend } from '@mui/x-charts/ChartsLegend/ChartsLegend'
import { ChartsTooltip } from '@mui/x-charts/ChartsTooltip/ChartsTooltip'
import { ChartsXAxis } from '@mui/x-charts/ChartsXAxis/ChartsXAxis'
import { ChartsYAxis } from '@mui/x-charts/ChartsYAxis/ChartsYAxis'
import { LinePlot } from '@mui/x-charts/LineChart/LinePlot'
import { ResponsiveChartContainer } from '@mui/x-charts/ResponsiveChartContainer'
import type { SeriesProviderProps } from '@mui/x-charts/context/SeriesProvider'
import dayjs from 'dayjs'
import type { SeriesModel } from 'evidently-ui-lib/api/types/v2'
import {
  Box,
  Card,
  CardContent,
  Divider,
  Skeleton,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { assertNever } from 'evidently-ui-lib/utils/index'
import { jsonToKeyValueRowString } from '../utils'

export type PlotPanelProps = {
  data: SeriesModel
  plotType: 'bar' | 'line'
  isStacked?: boolean
  title?: string
  description?: string
  height?: number
  legendMarginRight?: number
}

type SeriesType = SeriesProviderProps['series'][number]

export const PlotDashboardPanel = ({
  data,
  plotType,
  title,
  description,
  height = 350,
  legendMarginRight = 300,
  isStacked
}: PlotPanelProps) => {
  const series: SeriesType[] = data.series.map(({ values: data, params, metric_type }) => {
    const defaultLabel = `${metric_type.split(':').at(-1)}\n${jsonToKeyValueRowString(params)}`

    const common = {
      label: defaultLabel,
      stack: isStacked ? 'total' : undefined
    }

    if (plotType === 'line') {
      return { type: plotType, data, ...common } satisfies SeriesType
    }

    if (plotType === 'bar') {
      return { type: plotType, data, ...common } satisfies SeriesType
    }

    assertNever(plotType)
  })
  const xAxis = [
    {
      data: data.sources.map((e) => dayjs(e.timestamp).format('YYYY-MM-DD HH:mm:ss')),
      scaleType: 'band' as const
    }
  ]

  return (
    <Card elevation={0}>
      <CardContent>
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

        {(title || description) && <Divider sx={{ mb: 2, mt: 1 }} />}

        <Box height={height}>
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
          </ResponsiveChartContainer>
        </Box>
      </CardContent>
    </Card>
  )
}

export const DashboardPanelSkeleton = ({
  height = 350,
  title,
  subtitle
}: { height?: number; title?: string; subtitle?: string }) => {
  return (
    <Card elevation={0}>
      <CardContent>
        {title && (
          <Typography variant='h5' width={Math.max(title.length * 11, 450)}>
            <Skeleton variant='text' animation='wave' />
          </Typography>
        )}

        {subtitle && (
          <Typography>
            <Skeleton variant='text' animation='wave' />
          </Typography>
        )}

        {(title || subtitle) && <Divider sx={{ mb: 2, mt: 1 }} />}

        <Skeleton variant='rectangular' height={height} animation='wave' />
      </CardContent>
    </Card>
  )
}
