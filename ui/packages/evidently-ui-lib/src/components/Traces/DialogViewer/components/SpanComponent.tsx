import { KeyboardArrowDown } from '@mui/icons-material'
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Paper,
  Stack,
  Typography
} from '@mui/material'
import type { SpanModel } from 'api/types'
import { AttributesViewer } from './AttributesViewer'

type SpanComponentProps = {
  data: SpanModel
  spans: SpanModel[]
  traceStart: number
  totalTraceTime: number
  index: number
}
export const SpanComponent = (props: SpanComponentProps) => {
  const { data, spans, traceStart, totalTraceTime, index } = props

  const renderedSpans = spans.filter((s) => s.parent_span_id === data.span_id)
  return (
    <>
      <Stack>
        <Typography style={{ width: '200px', minWidth: '200px' }} variant={'body2'}>
          <b>{data.span_name}</b>
        </Typography>
      </Stack>
      <Paper sx={{ my: 2, p: 2, border: '1px solid', borderColor: 'divider' }}>
        <Box>
          {renderedSpans.length > 0 && (
            <Accordion
              sx={{
                border: 'none',
                borderTop: '1px solid',
                borderColor: 'divider',
                '&::before': { display: 'none' }
              }}
              slotProps={{ transition: { unmountOnExit: true, mountOnEnter: true } }}
            >
              <AccordionSummary expandIcon={<KeyboardArrowDown />}>
                <Typography variant='body2'>
                  <b>Spans</b>
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Paper sx={{ p: 2, border: '1px solid', borderColor: 'divider' }}>
                  {renderedSpans.map((s) => (
                    <SpanComponent
                      key={s.span_id}
                      data={s}
                      spans={spans}
                      traceStart={traceStart}
                      totalTraceTime={totalTraceTime}
                      index={index + 1}
                    />
                  ))}
                </Paper>
              </AccordionDetails>
            </Accordion>
          )}
        </Box>

        <AttributesViewer title={'Span Attributes'} data={data.attributes} />
      </Paper>
    </>
  )
}
