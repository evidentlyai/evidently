import { Card, Chip, Stack, Typography } from '@mui/material'
import { useTheme } from '@mui/material/styles'
import {
  ChartsAxisHighlight,
  ChartsAxisTooltipContent,
  ChartsGrid,
  ChartsTooltipContainer,
  ChartsXAxis,
  ChartsYAxis,
  LinePlot,
  useAxesTooltip,
  useDrawingArea,
  useXAxis
} from '@mui/x-charts'
import { BarPlot } from '@mui/x-charts'
import dayjs from 'dayjs'
import type { SeriesModel } from 'evidently-ui-lib/api/types'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { assertNever } from 'evidently-ui-lib/utils/index'
import { clamp } from 'evidently-ui-lib/utils/index'
import { useState } from 'react'
import { createContext, useContext } from 'react'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { useDashboardViewParams } from '~/contexts/DashboardViewParamsV2'
import { PanelCardGeneral } from './helpers/general'
import { MuiXChartPlotTemplate, type SeriesType, type XAxisType } from './helpers/mui'
import { getLabel } from './helpers/utils'

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

export const PlotDashboardPanel = ({
  data,
  type,
  title,
  description,
  height = 350,
  labels,
  isStacked
}: PlotPanelProps) => {
  const series: SeriesType[] = data.series.map(
    ({ values: data, params, metric_type, filter_index }) => {
      const { label } = getLabel({ metric_type, params, labels, filter_index })

      const common = {
        label,
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
      scaleType: 'band' as const,
      height: 50
    } satisfies XAxisType
  ]

  const viewParams = useDashboardViewParams()
  const OnClickComponent = viewParams?.OnClickedPointComponent

  const [highlightInfo, setHighlightInfo] = useState<{ index: number } | null>(null)

  const selectedSnapshotId = highlightInfo && data.sources[highlightInfo.index].snapshot_id

  return (
    <PanelCardGeneral title={title} description={description} height={height}>
      <DataContext.Provider value={{ data }}>
        <MuiXChartPlotTemplate
          series={series}
          xAxis={xAxis}
          SurfaceComponents={
            <>
              <BarLineSurfaceComponents />

              {OnClickComponent && (
                <>
                  <HighlightSelectionCustom onSelect={(index) => setHighlightInfo({ index })} />
                  {highlightInfo && <Highlight {...highlightInfo} />}
                </>
              )}
            </>
          }
        />

        {OnClickComponent && selectedSnapshotId && (
          <Box position={'relative'}>
            <Stack position={'absolute'} top={-20} right={-15}>
              <OnClickComponent snapshotId={selectedSnapshotId} />
            </Stack>
          </Box>
        )}
      </DataContext.Provider>
    </PanelCardGeneral>
  )
}

const DataContext = createContext<{ data: SeriesModel }>({
  data: { series: [], sources: [] }
})

const useDataContext = () => useContext(DataContext)

const CustomAxesTooltipContent = () => {
  const tooltipData = useAxesTooltip()

  const { data } = useDataContext()

  if (!tooltipData) {
    // No data to display
    return null
  }

  const dataIndex = tooltipData.at(0)?.dataIndex

  const tags = (typeof dataIndex === 'number' && data.sources?.[dataIndex]?.tags) || []

  return (
    <>
      {/* default */}
      <ChartsAxisTooltipContent />

      <Card
        sx={{
          backgroundColor: 'background.paper',
          borderTop: 'unset',
          p: 1,
          // hack to respect parent width
          width: 0,
          minWidth: '100%'
        }}
      >
        <Stack direction={'row'} flexWrap={'wrap'} gap={1}>
          <Typography>Report tags:</Typography>
          {tags.length === 0 && <Typography>None</Typography>}
          {tags.map((tag) => (
            <Chip key={tag} size='small' label={tag} />
          ))}
        </Stack>
      </Card>
    </>
  )
}

const BarLineSurfaceComponents = () => (
  <>
    <BarPlot />
    <LinePlot />

    <ChartsGrid horizontal />

    <ChartsXAxis label='Timestamps' position='bottom' labelStyle={{ fontSize: 18 }} />
    <ChartsYAxis position='left' />

    <ChartsAxisHighlight x={'band'} />

    <ChartsTooltipContainer trigger='axis'>
      <CustomAxesTooltipContent />
    </ChartsTooltipContainer>
  </>
)

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
      fill={theme.vars.palette.text.primary}
      shapeRendering={'crispEdges'}
      pointerEvents={'none'}
      opacity={0.1}
    />
  )
}
