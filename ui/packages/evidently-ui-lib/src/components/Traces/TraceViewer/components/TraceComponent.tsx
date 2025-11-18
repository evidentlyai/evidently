import { Close as CloseIcon } from '@mui/icons-material'
import {
  Box,
  Button,
  Chip,
  Collapse,
  Fade,
  IconButton,
  Stack,
  type SxProps,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  type Theme,
  Typography
} from '@mui/material'
import type { SpanModel } from 'api/types'
import type { TraceModel } from 'api/types'
import dayjs from 'dayjs'
import { useRef } from 'react'
import type React from 'react'
import { calculateTimeDifference } from '~/components/Traces/TraceViewer/helpers'
import {
  extractGuardRailsDataFromSpan,
  removeGuardRailsDataFromSpan
} from '~/components/Traces/TraceViewer/utils'
import { useTimeout } from '~/hooks'
import { AttributesViewer } from './AttributesViewer'
import { GuardRailStatus } from './GuardRailStatus'
import { SpanComponent } from './SpanComponent'
import { TextWithCopyButton } from './TextWithCopyButton'

type TraceComponentProps = {
  data: TraceModel
  showTimeline: boolean
  setSpanId: React.Dispatch<React.SetStateAction<string>>
  spanId: string
  collapsedSpanIds: string[]
  setCollapsedSpanIds: React.Dispatch<React.SetStateAction<string[]>>
}

export const TraceComponent = (props: TraceComponentProps) => {
  const { data, showTimeline, setSpanId, spanId, collapsedSpanIds, setCollapsedSpanIds } = props

  const startTime = dayjs(data.start_time).locale('en-gb')
  const endTime = dayjs(data.end_time).locale('en-gb')
  const totalTraceTime = endTime.valueOf() - startTime.valueOf()

  const spanToParents: [string, string[]][] = data.spans.map((s, _, arr) => [
    s.span_id,
    arr.filter((e) => e.parent_span_id === s.span_id).map((e) => e.span_id)
  ])

  const selectedSpan = data.spans.find((e) => e.span_id === spanId)

  const calcTotalShare = (span: SpanModel) =>
    Math.round(
      ((dayjs(span.end_time).valueOf() - dayjs(span.start_time).valueOf()) / totalTraceTime) * 1000
    ) / 10

  const childSelectedSpans = data.spans.filter((s) => s.parent_span_id === selectedSpan?.span_id)

  const sxArr: SxProps<Theme> = spanToParents.map(([s, p]) => ({
    [`:has(.spans-container .span-id-${s}:hover) :is(.span-id-${s},${p.map((s) => `.span-id-${s}`).join(',')})`]:
      (t) => ({
        backgroundColor: 'divider',
        ...t.applyStyles('light', { backgroundColor: '#e9e9e9' }),
        opacity: 1,
        transition: 'opacity background 0.2s cubic-bezier(0.4, 0, 1, 1)',
        cursor: 'pointer'
      }),
    [`.spans-container .span-id-${s}`]: {
      opacity: 1,
      transition: 'all 0.2s cubic-bezier(0.4, 0, 1, 1)'
    },
    [`:has(.spans-container:hover) .span-id-${s}`]: { opacity: 0.5 }
  }))

  const spanIds = data.spans.map((s) => s.span_id)
  const rootSpans = data.spans.filter(
    (s) => s.parent_span_id === '' || spanIds.indexOf(s.parent_span_id) < 0
  )

  const guardRailsData = selectedSpan ? extractGuardRailsDataFromSpan(selectedSpan) : null

  const { isOver: isMounted } = useTimeout()
  const timelineContainerRef = useRef<HTMLDivElement>(null)

  return (
    <Stack>
      <Box>
        <Box p={3} sx={sxArr}>
          <Box
            display={'grid'}
            gridTemplateColumns={`20% ${showTimeline ? (selectedSpan ? 35 : 80) : 0}% ${showTimeline ? (selectedSpan ? 45 : 0) : 80}%`}
            alignItems={'stretch'}
            sx={{ transition: '325ms ease-in-out' }}
          >
            <Box
              pt={4}
              borderRight={'1px solid'}
              borderColor={'divider'}
              sx={[{ overflowX: 'scroll' }]}
              className='spans-container'
            >
              {rootSpans.map((span) => (
                <SpanComponent
                  key={span.span_id}
                  setSpanId={setSpanId}
                  spanId={spanId}
                  collapsedSpanIds={collapsedSpanIds}
                  setCollapsedSpanIds={setCollapsedSpanIds}
                  span={span}
                  spans={data.spans}
                  traceStart={startTime.valueOf()}
                  totalTraceTime={totalTraceTime}
                  timelineContainer={timelineContainerRef}
                  isMounted={isMounted}
                />
              ))}
            </Box>

            <Box overflow={'hidden'} pt={4}>
              <Box position={'relative'} width={1}>
                <Box position={'absolute'} sx={{ top: -30 }} width={1} px={2}>
                  <Box height={'24.5px'} width={1}>
                    <Stack
                      direction={'row'}
                      justifyContent={'space-between'}
                      width={1}
                      alignItems={'center'}
                      gap={2}
                      divider={
                        <Box
                          flex={1}
                          height={'2px'}
                          sx={{ backgroundColor: 'divider', borderRadius: 0.5 }}
                        />
                      }
                    >
                      <Chip size='small' label={0} />

                      <Chip
                        size='small'
                        label={calculateTimeDifference(data.start_time, data.end_time)}
                      />
                    </Stack>
                  </Box>
                </Box>
              </Box>

              <Box className='spans-container' ref={timelineContainerRef} />
            </Box>

            <Box borderLeft={'1px solid'} borderColor={'divider'}>
              <Box sx={{ position: 'sticky', top: 15, left: 0, zIndex: 3 }}>
                <Fade key={data.trace_id} in={Boolean(selectedSpan)} timeout={500}>
                  <Box>
                    {selectedSpan && (
                      <Box px={3}>
                        <Box
                          display={'flex'}
                          justifyContent={'space-between'}
                          alignContent={'center'}
                        >
                          <Typography variant='h5'>{selectedSpan.span_name}</Typography>
                          <IconButton onClick={() => setSpanId('')}>
                            <CloseIcon fontSize='medium' />
                          </IconButton>
                        </Box>

                        <Box my={4}>
                          <AttributesViewer
                            alterBackgroundOdd={false}
                            data={{
                              Duration: calculateTimeDifference(
                                selectedSpan.start_time,
                                selectedSpan.end_time
                              ),
                              'Total share': `${calcTotalShare(selectedSpan)}%`,
                              'Child spans': childSelectedSpans.length
                            }}
                          />
                        </Box>

                        <Box my={4}>
                          <Typography variant='h6'>Span attributes</Typography>
                          <Box sx={{ overflow: 'scroll' }}>
                            <AttributesViewer
                              data={removeGuardRailsDataFromSpan(selectedSpan).attributes}
                              alterBackgroundOdd
                            />
                          </Box>
                        </Box>

                        {guardRailsData && guardRailsData.length > 0 && (
                          <Box my={4}>
                            <Stack gap={2}>
                              {guardRailsData.map(({ id, spanId, ...guardRail }, index) => (
                                <Box key={`${id}-${guardRail.name}-${index}`}>
                                  <Typography variant='h6'>{`${guardRail.name} Guard Rail`}</Typography>

                                  <Box sx={{ overflow: 'scroll' }}>
                                    <Table size='small'>
                                      <TableBody>
                                        {Object.entries(guardRail).map(([k, v]) => (
                                          <TableRow
                                            key={k}
                                            sx={{
                                              '&:nth-of-type(odd)': { backgroundColor: 'divider' }
                                            }}
                                          >
                                            <TableCell>
                                              <Typography>{k}</Typography>
                                            </TableCell>
                                            <TableCell>
                                              {k === 'status' ? (
                                                <Stack
                                                  direction={'row'}
                                                  justifyContent={'flex-end'}
                                                >
                                                  <GuardRailStatus
                                                    guardRailStatus={guardRail.status}
                                                  />
                                                </Stack>
                                              ) : (
                                                <TextWithCopyButton text={String(v)} />
                                              )}
                                            </TableCell>
                                          </TableRow>
                                        ))}
                                      </TableBody>
                                    </Table>
                                  </Box>
                                </Box>
                              ))}
                            </Stack>
                          </Box>
                        )}

                        <Box my={4}>
                          <Stack py={2} direction={'row'} gap={1} justifyContent={'space-between'}>
                            {childSelectedSpans.length > 0 && (
                              <Typography variant='h6'>Child spans</Typography>
                            )}

                            <Stack direction={'row'} gap={1}>
                              <Collapse
                                in={collapsedSpanIds.includes(selectedSpan.span_id)}
                                mountOnEnter
                                unmountOnExit
                              >
                                <Button
                                  size='small'
                                  variant='outlined'
                                  onClick={() =>
                                    setCollapsedSpanIds((p) =>
                                      p.filter((e) => e !== selectedSpan.span_id)
                                    )
                                  }
                                >
                                  Expand to see childs
                                </Button>
                              </Collapse>
                              <Collapse in={Boolean(selectedSpan.parent_span_id)}>
                                <Box>
                                  <Button
                                    size='small'
                                    variant='outlined'
                                    onClick={() => setSpanId(selectedSpan.parent_span_id)}
                                  >
                                    Go to parent
                                  </Button>
                                </Box>
                              </Collapse>
                            </Stack>
                          </Stack>

                          {childSelectedSpans.length > 0 && (
                            <Table size='small'>
                              <TableHead>
                                <TableRow>
                                  <TableCell>Span</TableCell>
                                  <TableCell>Total share</TableCell>
                                  <TableCell>Duration</TableCell>
                                </TableRow>
                                <TableRow />
                              </TableHead>
                              <TableBody className='spans-container'>
                                {childSelectedSpans.map((span) => (
                                  <TableRow
                                    key={span.span_id}
                                    className={`span-id-${span.span_id}`}
                                    onClick={() => {
                                      setSpanId(span.span_id)
                                      setCollapsedSpanIds((p) =>
                                        p.includes(span.span_id)
                                          ? p.filter((e) => e !== span.span_id)
                                          : p
                                      )
                                    }}
                                  >
                                    <TableCell>
                                      <Typography>{span.span_name}</Typography>
                                    </TableCell>

                                    <TableCell>
                                      <Typography>{`${calcTotalShare(span)}%`}</Typography>
                                    </TableCell>

                                    <TableCell>
                                      {calculateTimeDifference(span.start_time, span.end_time)}
                                    </TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          )}
                        </Box>
                      </Box>
                    )}
                  </Box>
                </Fade>
              </Box>
            </Box>
          </Box>
        </Box>
      </Box>
    </Stack>
  )
}
