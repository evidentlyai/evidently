import {
  BarPlot,
  ChartsAxisHighlight,
  ChartsGrid,
  ChartsLegend,
  ChartsTooltip,
  ChartsXAxis,
  ChartsYAxis,
  LinePlot
} from '@mui/x-charts'
import { ResponsiveChartContainer } from '@mui/x-charts/ResponsiveChartContainer'
import type { SeriesProviderProps } from '@mui/x-charts/context/SeriesProvider'
import type { SeriesModel } from 'api/types'
import {
  Box,
  Card,
  CardContent,
  Divider,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import { assertNever } from 'evidently-ui-lib/utils/index'

type SeriesType = SeriesProviderProps['series'][number]

type PanelProps = {
  data: SeriesModel
  plotType: 'bar' | 'line'
  isStacked?: boolean
  title?: string
  description?: string
  height?: number
  legendMarginRight?: number
}

export const DashboardPanel = ({
  data,
  plotType,
  title,
  description,
  height = 350,
  legendMarginRight = 300,
  isStacked
}: PanelProps) => {
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
      data: data.sources.map((e) => e.timestamp),
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

// biome-ignore lint/complexity/noBannedTypes: fine
const jsonToKeyValueRowString = (o: Object) => {
  const result = Object.entries(o)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n')

  return result
}
