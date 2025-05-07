import type { DashboardPanelPlotModel } from '~/api/types/v2'
import { assertNever } from '~/utils'
import type { DashboardPanelProps } from './Panels/DashboardPanel'

type Series = Partial<
  // biome-ignore lint/complexity/noBannedTypes: fine
  Record<'metric_labels' | 'metric' | 'metric_type', Object | null | undefined>
> &
  Partial<Record<'tags', string[] | null>>

export const getSeriesTypeHash = (s: Series) =>
  `${s.metric ?? s.metric_type}:${JSON.stringify(s?.tags?.toSorted())}:${JSON.stringify(s.metric_labels)}`

export const getSeriesListTypeHash = (seriesList: Series[]) =>
  seriesList.map(getSeriesTypeHash).join('|')

export const getSizeForGridItem = (size: 'half' | 'full') => {
  if (size === 'full') {
    return { xs: 12, sm: 12, md: 12, lg: 12 }
  }
  if (size === 'half') {
    return { xs: 12, sm: 12, md: 6, lg: 6 }
  }

  assertNever(size)
}

export const castRawPanelDataToDashboardPanelProps = (
  panel: DashboardPanelPlotModel
): DashboardPanelProps => {
  const emptyData = { series: [], sources: [] }
  const title = panel.title ?? ''
  const description = panel.subtitle ?? ''
  const height = 350

  const originalType = panel.plot_params?.plot_type

  const type = (originalType === 'line' ||
  originalType === 'bar' ||
  originalType === 'text' ||
  originalType === 'counter' ||
  originalType === 'pie'
    ? originalType
    : // trying cast to line
      'line') satisfies DashboardPanelProps['type'] as DashboardPanelProps['type']

  const originalAggregation = panel.plot_params?.aggregation

  const aggregation: 'last' | 'sum' | 'avg' =
    originalAggregation === 'last' || originalAggregation === 'sum' || originalAggregation === 'avg'
      ? originalAggregation
      : 'last'

  const size = panel.size === 'full' || panel.size === 'half' ? panel.size : 'full'

  const labels = panel.values.map((e) => e.legend)

  if (type === 'text') {
    return { type, size, title, description }
  }

  if (type === 'counter') {
    return { type, size, title, description, aggregation, data: emptyData, labels }
  }

  if (type === 'pie') {
    return { type, size, title, description, aggregation, data: emptyData, labels, height }
  }

  if (type === 'bar' || type === 'line') {
    const isStacked = Boolean(panel.plot_params?.is_stacked)

    return {
      type,
      size,
      title,
      description,
      isStacked,
      data: emptyData,
      labels,
      height
    }
  }

  assertNever(type)
}
