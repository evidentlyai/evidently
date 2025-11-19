import { Portal } from '@mui/material'
import { useState } from 'react'
import type { TraceModel } from '~/api/types'
import { TraceToolbar } from '~/components/Traces/TraceViewer/components/TraceToolbar'
import { useTraceToolbarRef } from '~/contexts/TraceToolbarContext'
import { SingleTraceView } from './components/SingleTraceView'
import { TraceTable } from './components/TraceTable'

type TraceViewerProps = {
  data: TraceModel[]
  onDelete: (traceId: string) => void
  defaultTraceId?: string
  isLoading: boolean
}

export const TraceViewer = (props: TraceViewerProps) => {
  const { data, onDelete, defaultTraceId, isLoading } = props

  const [traceId, setTraceId] = useState<string>(defaultTraceId ?? '')
  const selectedTrace = data.find((e) => e.trace_id === traceId)

  const traceToolbarRef = useTraceToolbarRef()

  const currentTraceIndex = data.findIndex((trace) => trace === selectedTrace)

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

      <SingleTraceView trace={selectedTrace} isLoading={isLoading} />
    </>
  )
}
