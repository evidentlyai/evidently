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
