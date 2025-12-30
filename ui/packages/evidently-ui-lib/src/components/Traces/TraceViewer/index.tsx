import { Close as CloseIcon } from '@mui/icons-material'
import { Box, Fade, IconButton, Portal, Stack, Typography } from '@mui/material'
import dayjs from 'dayjs'
import { useState } from 'react'
import type { TraceModel } from '~/api/types'
import { TraceToolbar } from '~/components/Traces/TraceViewer/components/TraceToolbar'
import { extractGuardRailsDataFromSpan } from '~/components/Traces/TraceViewer/utils'
import { useTraceToolbarRef } from '~/contexts/TraceToolbarContext'
import { isNotNull } from '~/utils'
import { CostComponent } from './components/CostComponent'
import { DurationComponent } from './components/DurationComponent'
import { GuardRailsShowInfoButton } from './components/GuardRailsShowInfoButton'
import { InfoBlock } from './components/InfoBlock'
import { ShowTraceComponentToggle } from './components/ShowTraceComponentToggle'
import { StartTimeComponent } from './components/StartTimeComponent'
import { TimelineToggle } from './components/TimelineToggle'
import { TraceComponent as TraceComponentView } from './components/TraceComponent'
import { TraceTable } from './components/TraceTable'
import { ExtractUsageData } from './helpers'

type TraceViewerProps = {
  data: TraceModel[]
  onDelete: (traceId: string) => void
  defaultTraceId?: string
  isLoading: boolean
  traceComponent: (props: { trace: TraceModel }) => React.ReactNode
}

export const TraceViewer = (props: TraceViewerProps) => {
  const { data, onDelete, defaultTraceId, isLoading, traceComponent } = props

  const [traceId, setTraceId] = useState<string>(defaultTraceId ?? '')
  const [showTraceComponent, setShowTraceComponent] = useState(false)
  const selectedTrace = data.find((e) => e.trace_id === traceId)

  const traceToolbarRef = useTraceToolbarRef()

  const currentTraceIndex = data.findIndex((trace) => trace === selectedTrace)

  // Inlined from SingleTraceView
  const [showTimeline, setShowTimeline] = useState(true)
  const [collapsedSpanIds, setCollapsedSpanIds] = useState<Array<string>>([])
  const [spanId, setSpanId] = useState('')

  const extractUsageData = selectedTrace ? ExtractUsageData(selectedTrace) : new Map()
  const totalTokens = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][0], 0)
  const totalCost = Array.from(extractUsageData.entries()).reduce((acc, it) => acc + it[1][1], 0)

  const guardRailsData = selectedTrace
    ? selectedTrace.spans.map(extractGuardRailsDataFromSpan).filter(isNotNull).flat()
    : []
  const selectedSpan = selectedTrace
    ? selectedTrace.spans.find((span) => span.span_id === spanId)
    : undefined

  if (selectedTrace && spanId && !selectedSpan) {
    const rootSpan = selectedTrace.spans.find((s) => s.parent_span_id === '')

    setSpanId(rootSpan?.span_id ?? '')
    setCollapsedSpanIds([])
  }

  if (traceId && !selectedTrace) {
    setTraceId('')
  }

  if (!selectedTrace) {
    return (
      <TraceTable data={data} onSelect={setTraceId} onDelete={onDelete} isLoading={isLoading} />
    )
  }

  return (
    <>
      <Portal container={() => traceToolbarRef.current}>
        <TraceToolbar
          traceIds={data.map((e) => e.trace_id)}
          traceId={traceId}
          onBackToTableView={() => setTraceId('')}
          onSelectTrace={setTraceId}
          goToNextTrace={() => {
            const nextTrace = data.at(currentTraceIndex + 1)
            if (nextTrace) {
              setTraceId(nextTrace.trace_id)
            }
          }}
          goToPreviousTrace={() => {
            const previousTrace = data.at(currentTraceIndex - 1)
            if (previousTrace) {
              setTraceId(previousTrace.trace_id)
            }
          }}
          isPossibleToGoToNextTrace={currentTraceIndex < data.length - 1}
          isPossibleToGoToPreviousTrace={currentTraceIndex > 0}
        />
      </Portal>

      <Stack direction={'row'} gap={2}>
        <StartTimeComponent value={dayjs(selectedTrace.start_time)} />
        <DurationComponent
          value={dayjs(selectedTrace.end_time).diff(dayjs(selectedTrace.start_time), 'ms')}
        />
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

        <ShowTraceComponentToggle
          showTraceComponent={showTraceComponent}
          setShowTraceComponent={setShowTraceComponent}
        />
      </Stack>

      <Box
        display='grid'
        gridTemplateColumns={showTraceComponent ? '70% 30%' : '100% 0'}
        sx={{ transition: '325ms ease-in-out' }}
      >
        <TraceComponentView
          data={selectedTrace}
          showTimeline={showTimeline}
          setSpanId={setSpanId}
          spanId={spanId}
          collapsedSpanIds={collapsedSpanIds}
          setCollapsedSpanIds={setCollapsedSpanIds}
        />

        <Fade in={showTraceComponent} timeout={800} exit={false}>
          <Box borderLeft={1} borderColor={'divider'}>
            <Box position='sticky' top={15}>
              <Stack gap={2} p={3}>
                <Stack direction='row' alignItems='center' justifyContent='space-between'>
                  <Typography variant='h5'>Feedback</Typography>

                  <IconButton onClick={() => setShowTraceComponent(false)} size='small'>
                    <CloseIcon />
                  </IconButton>
                </Stack>

                {traceComponent({ trace: selectedTrace })}
              </Stack>
            </Box>
          </Box>
        </Fade>
      </Box>
    </>
  )
}
