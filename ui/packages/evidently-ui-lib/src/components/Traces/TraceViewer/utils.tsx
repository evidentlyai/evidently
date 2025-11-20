import type { SpanModel } from 'api/types'

export type GuardRailData = {
  spanId: string
  id: string
  name: string
  status: string
  error?: string
}

const GUARD_RAIL_PREFIX = 'evidently.guardrail.'

export const extractGuardRailsDataFromSpan = (span: SpanModel): GuardRailData[] => {
  const guardRailData: Record<string, GuardRailData> = {}

  for (const [spanAttr, spanValue] of Object.entries(span.attributes)) {
    const guardAttr = spanAttr.split('.').at(-1)
    const guardId = spanAttr.split('.').at(2)

    if (
      !spanAttr.startsWith(GUARD_RAIL_PREFIX) ||
      !guardId ||
      !(guardAttr === 'name' || guardAttr === 'status' || guardAttr === 'error')
    ) {
      continue
    }

    const guardIdUniqueAcrossSpans = `span-${span.span_id}-giard-${guardId}`

    if (!guardRailData[guardIdUniqueAcrossSpans]) {
      guardRailData[guardIdUniqueAcrossSpans] = {
        id: guardIdUniqueAcrossSpans,
        spanId: span.span_id,
        name: '',
        status: ''
      }
    }

    guardRailData[guardIdUniqueAcrossSpans][guardAttr] = String(spanValue)
  }

  return Object.values(guardRailData)
}

export const removeGuardRailsDataFromSpan = (span: SpanModel): SpanModel => ({
  ...span,
  attributes: Object.fromEntries(
    Object.entries(span.attributes).filter(([key]) => !key.startsWith(GUARD_RAIL_PREFIX))
  )
})
