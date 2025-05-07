import { Stack, type SxProps } from '@mui/material'
import {
  ChartDataProvider,
  ChartsLegend,
  ChartsSurface,
  MarkPlot,
  blueberryTwilightPalette
} from '@mui/x-charts'
import type {
  UseChartCartesianAxisParameters,
  UseChartSeriesParameters
} from '@mui/x-charts/internals'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'

export type SeriesType = Exclude<UseChartSeriesParameters['series'], undefined>[number]
export type XAxisType = Exclude<UseChartCartesianAxisParameters['xAxis'], undefined>[number]

export const MuiXChartPlotTemplate = ({
  series,
  xAxis,
  SurfaceComponents,
  sxChartsSurface
}: {
  series: SeriesType[]
  xAxis?: XAxisType[]
  SurfaceComponents?: React.ReactNode
  sxChartsSurface?: SxProps
}) => {
  return (
    <>
      <ChartDataProvider series={series} xAxis={xAxis} colors={blueberryTwilightPalette}>
        <Stack direction={'row'} gap={1} height={'100%'}>
          <ChartsSurface
            sx={[...(Array.isArray(sxChartsSurface) ? sxChartsSurface : [sxChartsSurface])]}
          >
            {SurfaceComponents && SurfaceComponents}

            <MarkPlot />
          </ChartsSurface>

          <Box maxWidth={300}>
            <CustomChartLegend />
          </Box>
        </Stack>
      </ChartDataProvider>
    </>
  )
}

const CustomChartLegend = () => (
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
)
