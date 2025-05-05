import type { DashboardPanelPlotModel } from '~/api/types/v2'
import { assertNever } from '~/utils'
import type { DashboardPanelProps } from './Panels/DashboardPanel'
import type { CounterPanelProps } from './Panels/implementations/Counter'

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

export const formatLabelWithParams = ({
  label,
  params
}: {
  label: string
  params: Record<string, string | undefined>
}) => {
  const result = label.replace(
    /\{\{([a-zA-Z_0-9]+)?\}\}/g,
    (_, key) => params?.[key] ?? `{{${key}}}`
  )

  return result
}

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

  const originalType = panel.plot_params?.plot_type

  const type: DashboardPanelProps['type'] =
    (originalType === 'line' ||
    originalType === 'bar' ||
    originalType === 'text' ||
    originalType === 'counter'
      ? originalType
      : null) ?? 'line'

  const size = panel.size === 'full' || panel.size === 'half' ? panel.size : 'full'

  const labels = panel.values.map((e) => e.legend)

  if (type === 'text') {
    return { type, size, title, description }
  }

  if (type === 'counter') {
    const originalCounterAgg = panel.plot_params?.aggregation

    const counterAgg: CounterPanelProps['counterAgg'] =
      originalCounterAgg === 'last' || originalCounterAgg === 'sum' || originalCounterAgg === 'avg'
        ? originalCounterAgg
        : 'last'

    return { type, size, title, description, counterAgg, data: emptyData, labels }
  }

  if (type === 'bar' || type === 'line') {
    const height = 350
    const isStacked = Boolean(panel.plot_params?.is_stacked)

    return {
      type,
      size,
      title,
      description,
      isStacked,

      height,
      data: emptyData,
      labels
    }
  }

  assertNever(type)
}
