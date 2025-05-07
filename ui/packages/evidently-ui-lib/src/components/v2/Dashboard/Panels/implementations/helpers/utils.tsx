const DEFAULT_ROUND_DIGITS = 2

export const getAggValue = (
  data: (number | null)[],
  counterAgg: 'last' | 'sum' | 'avg',
  round?: number
) => {
  const result = _getAggValueInternal(data, counterAgg)

  if (!result) {
    return 'no value'
  }

  const roundedResult = Number.parseFloat(result.toFixed(round ?? DEFAULT_ROUND_DIGITS))

  return roundedResult
}

const _getAggValueInternal = (data: (number | null)[], counterAgg: 'last' | 'sum' | 'avg') => {
  const getSum = () => data.reduce((prev, curr) => (prev ?? 0) + (curr ?? 0), 0)

  if (data.length === 0) {
    return null
  }

  if (counterAgg === 'last') {
    return data.at(-1)
  }

  if (counterAgg === 'sum') {
    return getSum()
  }

  if (counterAgg === 'avg') {
    return (getSum() ?? 0) / data.length
  }
}

export const getLabel = ({
  metric_type,
  params,
  labels,
  filter_index
}: {
  metric_type: string
  params: { [key: string]: string }
  labels: (string | undefined | null)[]
  filter_index: number
}) => {
  const metricName = metric_type.split(':').at(-1)
  const defaultLabel = [metricName, jsonToKeyValueRowString(params)].filter(Boolean).join('\n')

  const customLabel = formatLabelWithParams({ label: labels?.[filter_index] ?? '', params })

  const label = customLabel || defaultLabel

  return { label, defaultLabel }
}

// biome-ignore lint/complexity/noBannedTypes: fine
const jsonToKeyValueRowString = (o: Object) => {
  const result = Object.entries(o)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n')

  return result
}

const formatLabelWithParams = ({
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
