import { ChartsTooltip, PiePlot, pieArcLabelClasses } from '@mui/x-charts'
import type { SeriesModel } from 'evidently-ui-lib/api/types'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { PanelCardGeneral } from './helpers/general'
import { MuiXChartPlotTemplate, type SeriesType } from './helpers/mui'
import { getAggValue, getLabel } from './helpers/utils'

export type PiePanelProps = MakePanel<{
  type: 'pie'
  title?: string
  description?: string
  data: SeriesModel
  labels: (string | undefined | null)[]
  size: 'full' | 'half'
  aggregation: 'last' | 'sum' | 'avg'
  height?: number
  borderNone?: boolean
}>

export const PieDashboardPanel = ({
  data,
  title,
  description,
  height = 350,
  labels,
  aggregation,
  borderNone = false
}: PiePanelProps) => {
  const pieData = data.series.map(({ values: data, params, metric_type, filter_index }) => {
    const { label } = getLabel({ metric_type, params, labels, filter_index })

    const value = getAggValue(data, aggregation)

    return {
      label,
      labelMarkType: 'circle' as const,
      value: value === 'no value' ? 0 : value,
      // trying to guess color
      ...(/\bFAIL\b|\bFAILED\b/gi.test(label) ? { color: '#b70000' } : {}),
      ...(/\bSUCCESS\b|\bPASS\b|\bPASSED\b|\bOK\b/gi.test(label) ? { color: '#098249' } : {}),
      ...(/\bWARNING\b/gi.test(label) ? { color: '#ffad01' } : {}),
      ...(/\bERROR\b/gi.test(label) ? { color: '#6B8BA4' } : {})
    }
  })

  const total = pieData.reduce((prev, cur) => prev + cur.value, 0)

  const calculateShare = (value: number) => Number.parseFloat(((value / total) * 100).toFixed())
  const getArcLabel = ({ value }: { value: number }) => `${value} (${calculateShare(value)}%)`
  const [valueFormatter, arcLabel] = [getArcLabel, getArcLabel]

  const series: SeriesType[] = [
    {
      type: 'pie',
      highlightScope: { fade: 'global', highlight: 'item' },
      faded: { additionalRadius: -30, color: 'gray' },
      arcLabelMinAngle: 25,
      data: pieData,
      valueFormatter,
      arcLabel
    }
  ]

  return (
    <PanelCardGeneral
      title={title}
      description={description}
      height={height}
      textCenterAlign
      borderNone={borderNone}
    >
      <MuiXChartPlotTemplate
        series={series}
        SurfaceComponents={<PieSurfaceComponents />}
        sxChartsSurface={{ [`& .${pieArcLabelClasses.root}`]: { fontWeight: 'bold' } }}
      />
    </PanelCardGeneral>
  )
}

const PieSurfaceComponents = () => (
  <>
    <PiePlot />
    <ChartsTooltip trigger={'item'} />
  </>
)
