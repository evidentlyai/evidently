import type { DashboardPanelPlotModel } from '~/api/types/v2'
import type { DashboardPanelProps } from './DashboardPanel'

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
): // @ts-ignore
DashboardPanelProps => {
  const originalPlotType = panel.plot_params?.plot_type

  // @ts-ignore
  const plotType: DashboardPanelProps['plotType'] =
    (originalPlotType === 'line' ||
    originalPlotType === 'bar' ||
    originalPlotType === 'text' ||
    originalPlotType === 'counter'
      ? originalPlotType
      : null) ?? 'line'

  // if (plotType === 'bar' || plotType === 'text') {
  //   return {}
  // }
}
