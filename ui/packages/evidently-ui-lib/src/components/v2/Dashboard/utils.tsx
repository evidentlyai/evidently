import type { DashboardPanelPlotModel } from '~/api/types/v2'
import { assertNever } from '~/utils'
import type { DashboardPanelProps } from './DashboardPanel'
import type { CounterPanelProps } from './Panels/Counter'

type Series = Partial<
  // biome-ignore lint/complexity/noBannedTypes: fine
  Record<'metric_labels' | 'metric' | 'metric_type', Object | null | undefined>
> &
  Partial<Record<'tags', string[] | null>>

export const getSeriesTypeHash = (s: Series) =>
  `${s.metric ?? s.metric_type}:${JSON.stringify(s?.tags?.toSorted())}:${JSON.stringify(s.metric_labels)}`

export const getSeriesListTypeHash = (seriesList: Series[]) =>
  seriesList.map(getSeriesTypeHash).join('|')

// biome-ignore lint/complexity/noBannedTypes: fine
export const jsonToKeyValueRowString = (o: Object) => {
  const result = Object.entries(o)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n')

  return result
}

export const castRawPanelDataToDashboardPanelProps = (
  panel: DashboardPanelPlotModel
): DashboardPanelProps => {
  const emptyData = { series: [], sources: [] }
  const title = panel.title ?? ''
  const description = panel.subtitle ?? ''

  const originalPlotType = panel.plot_params?.plot_type

  const plotType: DashboardPanelProps['plotType'] =
    (originalPlotType === 'line' ||
    originalPlotType === 'bar' ||
    originalPlotType === 'text' ||
    originalPlotType === 'counter'
      ? originalPlotType
      : null) ?? 'line'

  if (plotType === 'text') {
    return { plotType: plotType, title, description }
  }

  if (plotType === 'counter') {
    const originalCounterAgg = panel.plot_params?.aggregation
    const counterAgg: CounterPanelProps['counterAgg'] =
      originalCounterAgg === 'last' || originalCounterAgg === 'sum' || originalCounterAgg === 'avg'
        ? originalCounterAgg
        : 'last'

    return { plotType: plotType, data: emptyData, title, description, counterAgg }
  }

  if (plotType === 'bar' || plotType === 'line') {
    const height = 350
    const isStacked = Boolean(panel.plot_params?.is_stacked)

    const legendMarginRight =
      typeof panel.plot_params?.legend_margin_right === 'number'
        ? Number(panel.plot_params?.legend_margin_right)
        : 300

    return {
      plotType,
      data: emptyData,
      title,
      description,
      isStacked,
      legendMarginRight,
      height
    }
  }

  assertNever(plotType)
}
