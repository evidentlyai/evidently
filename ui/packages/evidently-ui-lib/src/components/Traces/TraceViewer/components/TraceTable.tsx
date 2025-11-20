import { Delete as DeleteIcon } from '@mui/icons-material'
import { Button, IconButton, Stack, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import type { TraceModel } from '~/api/types'
import { GenericTable } from '~/components/Table/GenericTable'
import { calculateTimeDifference } from '~/components/Traces/TraceViewer/helpers'
import { extractGuardRailsDataFromSpan } from '~/components/Traces/TraceViewer/utils'

import { isNotNull } from '~/utils'
import { GuardRailsShowInfoButton } from './GuardRailsShowInfoButton'
import { UsageData } from './UsageData'

type TraceTableProps = {
  data: TraceModel[]
  onSelect: (traceId: string) => void
  onDelete: (traceId: string) => void
  isLoading: boolean
}

export const TraceTable = (props: TraceTableProps) => {
  const { data, onSelect, onDelete, isLoading } = props

  return (
    <GenericTable
      data={data}
      idField='trace_id'
      isLoading={isLoading}
      emptyMessage="You don't have any traces yet."
      columns={[
        {
          key: 'trace_id',
          label: 'Trace ID',
          sortable: { getSortValue: (trace) => trace.trace_id },
          render: (trace) => <Typography variant='body2'>{trace.trace_id}</Typography>
        },
        {
          key: 'start_time',
          label: 'Start time',
          sortable: { getSortValue: (trace) => trace.start_time, isDateString: true },
          render: (trace) => (
            <Typography variant='body2'>
              {dayjs(trace.start_time).locale('en-gb').format('ddd, MMM D, YYYY h:mm:ss A')}
            </Typography>
          )
        },
        {
          key: 'end_time',
          label: 'End time',
          sortable: { getSortValue: (trace) => trace.end_time, isDateString: true },
          render: (trace) => (
            <Typography variant='body2'>
              {dayjs(trace.end_time).locale('en-gb').format('ddd, MMM D, YYYY h:mm:ss A')}
            </Typography>
          )
        },
        {
          key: 'duration',
          label: 'Duration',
          sortable: {
            getSortValue: (trace) => calculateTimeDifference(trace.start_time, trace.end_time)
          },
          render: (trace) => (
            <Typography variant='body2'>
              {calculateTimeDifference(trace.start_time, trace.end_time)}
            </Typography>
          )
        },
        {
          key: 'token_usage',
          label: 'Token usage',
          render: (trace) => <UsageData trace={trace} />
        },
        {
          key: 'guardrails',
          label: 'Guardrails',
          align: 'center',
          skipRender: data.every(
            (trace) =>
              trace.spans.map(extractGuardRailsDataFromSpan).filter(isNotNull).flat().length === 0
          ),
          render: (trace) => (
            <GuardRailsShowInfoButton
              guardRailData={trace.spans
                .map(extractGuardRailsDataFromSpan)
                .filter(isNotNull)
                .flat()}
            />
          )
        },
        {
          key: 'actions',
          label: 'Action',
          align: 'center',
          render: (trace) => (
            <Stack direction={'row'} width={1} justifyContent={'center'}>
              <Button onClick={() => onSelect(trace.trace_id)}>View</Button>
              <Tooltip title='delete'>
                <IconButton
                  disabled={isLoading}
                  size='small'
                  onClick={() => onDelete(trace.trace_id)}
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </Stack>
          )
        }
      ]}
    />
  )
}
