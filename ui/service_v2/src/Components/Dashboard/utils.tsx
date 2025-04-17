type Series = Partial<
  // biome-ignore lint/complexity/noBannedTypes: fine
  Record<'metric_labels' | 'metric' | 'metric_type', Object | null | undefined>
> &
  Partial<Record<'tags', string[] | null>>

export const getSeriesTypeHash = (s: Series) =>
  `${s.metric ?? s.metric_type}:${JSON.stringify(s?.tags?.toSorted())}:${JSON.stringify(s.metric_labels)}`

export const getSeriesListTypeHash = (seriesList: Series[]) =>
  seriesList.map(getSeriesTypeHash).join('|')
