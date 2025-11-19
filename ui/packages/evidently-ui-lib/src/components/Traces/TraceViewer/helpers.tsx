import dayjs from 'dayjs'
import type { TraceModel } from '~/api/types'

export function calculateTimeDifference(
  date1: string | Date,
  date2: string | Date | null | undefined
): string {
  if (!date2) {
    return ''
  }

  const diffMilliseconds = Math.abs(dayjs(date1).diff(dayjs(date2)))

  if (diffMilliseconds < 1000) {
    return `${diffMilliseconds} ms`
  }

  const diffSeconds = diffMilliseconds / 1000
  if (diffSeconds < 60) {
    return `${diffSeconds.toFixed(2)} s`
  }

  const diffMinutes = diffMilliseconds / (1000 * 60)
  return `${diffMinutes.toFixed(2)} m}`
}

export function ExtractUsageData(trace: TraceModel): Map<string, [number, number]> {
  return trace.spans.reduce((acc, it) => {
    Object.entries(it.attributes).map(([attr, value]) => {
      if (attr.startsWith('tokens.')) {
        const tokenId = attr.substring('tokens.'.length)
        const val = acc.has(tokenId) ? acc.get(tokenId) : [0, null]
        if (val[0] === null) {
          val[0] = 0
        }
        val[0] += typeof value === 'string' ? Number.parseInt(value) : value
        acc.set(tokenId, val)
      }
      if (attr.startsWith('cost.')) {
        const tokenId = attr.substring('cost.'.length)
        const val = acc.has(tokenId) ? acc.get(tokenId) : [null, 0]
        if (val[1] === null) {
          val[1] = 0.0
        }
        val[1] += typeof value === 'string' ? Number.parseFloat(value) : value
        acc.set(tokenId, val)
      }
    })
    return acc
  }, new Map())
}
