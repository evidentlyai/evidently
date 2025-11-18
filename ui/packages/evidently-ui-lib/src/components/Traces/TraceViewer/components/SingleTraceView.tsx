import { Stack } from '@mui/material'
import dayjs from 'dayjs'
import { useState } from 'react'
import type { TraceModel } from '~/api/types'
import { extractGuardRailsDataFromSpan } from '~/components/Traces/TraceViewer/utils'
import { isNotNull } from '~/utils'
import { ExtractUsageData } from '../helpers'
import { CostComponent } from './CostComponent'
import { DurationComponent } from './DurationComponent'
import { GuardRailsShowInfoButton } from './GuardRailsShowInfoButton'
import { InfoBlock } from './InfoBlock'
import { StartTimeComponent } from './StartTimeComponent'
import { TimelineToggle } from './TimelineToggle'
import { TraceComponent } from './TraceComponent'

type SingleTraceViewProps = { trace: TraceModel; isLoading: boolean }

export const SingleTraceView = (props: SingleTraceViewProps) => {
  const { trace, isLoading } = props

  const [showTimeline, setShowTimeline] = useState(true)
  const [collapsedSpanIds, setCollapsedSpanIds] = useState<Array<string>>([])
  const extractUsageData = ExtractUsageData(trace)
  const totalTokens = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][0], 0)
  const totalCost = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][1], 0)

  const guardRailsData = trace.spans.map(extractGuardRailsDataFromSpan).filter(isNotNull).flat()

  const [spanId, setSpanId] = useState('')
  const selectedSpan = trace.spans.find((span) => span.span_id === spanId)

  if (spanId && !selectedSpan) {
    setSpanId(trace.spans.at(0)?.span_id ?? '')
    setCollapsedSpanIds([])
  }

  return (
    <>
      <Stack direction='column'>
        <Stack direction={'row'} gap={2}>
          <StartTimeComponent value={dayjs(trace.start_time)} />
          <DurationComponent value={dayjs(trace.end_time).diff(dayjs(trace.start_time), 'ms')} />
          <CostComponent cost={totalCost} tokens={totalTokens} breakdown={extractUsageData} />

          {guardRailsData.length > 0 && (
            <InfoBlock title={'Guard rails'}>
              <GuardRailsShowInfoButton guardRailData={guardRailsData} onGoToSpan={setSpanId} />
            </InfoBlock>
          )}

          <TimelineToggle
            showTimeline={showTimeline}
            setShowTimeline={setShowTimeline}
            isLoading={isLoading}
          />
        </Stack>

        <TraceComponent
          data={trace}
          showTimeline={showTimeline}
          setSpanId={setSpanId}
          spanId={spanId}
          collapsedSpanIds={collapsedSpanIds}
          setCollapsedSpanIds={setCollapsedSpanIds}
        />
      </Stack>
    </>
  )
}
