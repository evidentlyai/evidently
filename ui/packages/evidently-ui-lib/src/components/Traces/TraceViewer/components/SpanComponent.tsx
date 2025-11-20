import { AddCircleOutline as AddCircleRoundedIcon } from '@mui/icons-material'
import { RemoveCircleOutline as RemoveCircleRoundedIcon } from '@mui/icons-material'
import { PolicyOutlined as PolicyOutlinedIcon } from '@mui/icons-material'
import { Box, Collapse, IconButton, Portal, Stack, Tooltip, Typography } from '@mui/material'
import dayjs from 'dayjs'
import type React from 'react'
import type { SpanModel } from '~/api/types'
import { calculateTimeDifference } from '~/components/Traces/TraceViewer/helpers'
import { extractGuardRailsDataFromSpan } from '~/components/Traces/TraceViewer/utils'
import { getGuardRailStatusColor } from './GuardRailStatus'

type SpanComponentProps = {
  span: SpanModel
  spans: SpanModel[]
  traceStart: number
  totalTraceTime: number
  spanId: string
  setSpanId: (s: string) => void
  timelineContainer: React.RefObject<HTMLElement>
  isMounted: boolean
  hide?: boolean
  collapsedSpanIds: string[]
  setCollapsedSpanIds: React.Dispatch<React.SetStateAction<string[]>>
}

export const SpanComponent = (props: SpanComponentProps) => {
  const {
    span,
    spans,
    traceStart,
    totalTraceTime,
    timelineContainer,
    isMounted,
    hide,
    spanId,
    setSpanId,
    collapsedSpanIds,
    setCollapsedSpanIds
  } = props

  const startTime = dayjs(span.start_time).valueOf()
  const endTime = dayjs(span.end_time).valueOf()

  const renderedSpans = spans.filter((s) => s.parent_span_id === span.span_id)

  const on = !collapsedSpanIds.includes(span.span_id)

  const guardRailsData = extractGuardRailsDataFromSpan(span)

  return (
    <Box sx={{ width: 'fit-content', minWidth: '100%' }}>
      <Stack
        direction={'row'}
        gap={0.5}
        alignItems={'center'}
        justifyItems={'center'}
        className={`span-id-${span.span_id}`}
        onClick={() => setSpanId(span.span_id)}
        sx={[
          { height: '24.5px' },
          spanId === span.span_id && {
            borderTop: '1px solid gray',
            borderBottom: '1px solid gray'
          }
        ]}
      >
        <Typography variant='button'>{span.span_name}</Typography>

        {renderedSpans.length > 0 && (
          <>
            <IconButton
              size='small'
              onClick={() =>
                setCollapsedSpanIds((p) =>
                  on ? [...p, span.span_id] : p.filter((e) => e !== span.span_id)
                )
              }
            >
              {on ? (
                <RemoveCircleRoundedIcon sx={{ fontSize: 14 }} />
              ) : (
                <AddCircleRoundedIcon sx={{ fontSize: 14 }} />
              )}
            </IconButton>

            {renderedSpans.length > 1 && (
              <Box>
                <Typography align='right' variant='body1' fontSize={'0.7rem'}>
                  ({renderedSpans.length})
                </Typography>
              </Box>
            )}
          </>
        )}

        {guardRailsData.map((guardRail) => (
          <Tooltip
            key={guardRail.id}
            title={`${guardRail.name} guardrail with ${getGuardRailStatusColor(guardRail.status)}`}
            placement='top'
          >
            <IconButton size='small'>
              <PolicyOutlinedIcon
                sx={{ fontSize: 14 }}
                color={getGuardRailStatusColor(guardRail.status)}
              />
            </IconButton>
          </Tooltip>
        ))}
      </Stack>

      {isMounted && (
        <Portal container={() => timelineContainer.current}>
          <Collapse in={!hide}>
            <Box
              height={'24.5px'}
              display={'flex'}
              alignItems={'center'}
              className={`span-id-${span.span_id}`}
              px={2}
              onClick={() => setSpanId(span.span_id)}
              sx={[
                spanId === span.span_id && {
                  borderTop: '1px solid gray',
                  borderBottom: '1px solid gray'
                }
              ]}
            >
              <Tooltip
                disableInteractive
                arrow
                placement='top'
                title={calculateTimeDifference(span.start_time, span.end_time)}
              >
                <Box
                  height={0.3}
                  width={
                    endTime - startTime === 0
                      ? 1e-3
                      : Number(((endTime - startTime) / totalTraceTime).toFixed(2))
                  }
                  ml={`${(((startTime - traceStart) / totalTraceTime) * 100).toFixed(2)}%`}
                  sx={(t) => ({
                    borderRadius: 0.5,
                    backgroundColor: 'error.light',
                    ...t.applyStyles('light', { backgroundColor: t.palette.grey['800'] })
                  })}
                />
              </Tooltip>
            </Box>
          </Collapse>
        </Portal>
      )}

      <Collapse in={on}>
        <Box sx={{ borderLeft: '1px solid', borderColor: 'divider', pl: 2, mt: 0 }}>
          {renderedSpans.map((span) => (
            <Box key={span.span_id}>
              <SpanComponent
                key={span.span_id}
                collapsedSpanIds={collapsedSpanIds}
                setCollapsedSpanIds={setCollapsedSpanIds}
                span={span}
                spans={spans}
                traceStart={traceStart}
                totalTraceTime={totalTraceTime}
                timelineContainer={timelineContainer}
                hide={hide || !on}
                spanId={spanId}
                setSpanId={setSpanId}
                isMounted={isMounted}
              />
            </Box>
          ))}
        </Box>
      </Collapse>
    </Box>
  )
}
