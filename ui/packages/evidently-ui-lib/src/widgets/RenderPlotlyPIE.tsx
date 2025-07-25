import type { AdditionalGraphInfo } from '~/api'
import { PieDashboardPanel } from '~/components/v2/Dashboard/Panels/implementations/Pie'

type RenderPlotlyPIEProps = AdditionalGraphInfo & {
  widgetSize: number
}

export const RenderPlotlyPIE = (props: RenderPlotlyPIEProps) => {
  const [pieData] = props.data

  return (
    <PieDashboardPanel
      borderNone
      type='pie'
      data={{
        series: (pieData.values?.map((value) => Number(value)) ?? []).map((e, filter_index) => ({
          filter_index,
          values: [e],
          params: {},
          metric_type: ''
        })),
        sources: []
      }}
      labels={pieData.labels?.map((label) => label?.toString()) ?? []}
      size={props.widgetSize === 1 ? 'half' : 'full'}
      aggregation={'last'}
    />
  )
}
