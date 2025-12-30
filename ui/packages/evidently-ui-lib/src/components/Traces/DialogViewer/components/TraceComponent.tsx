import { Stack } from '@mui/material'
import type { TraceModel } from 'api/types'
import dayjs from 'dayjs'
import { SplitField } from '../helpers'
import type { Description } from '../types'
import { Message } from './Message'

type TraceComponentProps = {
  data: TraceModel
  description: Description
  traceHeader?: React.ReactNode
}

export const TraceComponent = (props: TraceComponentProps) => {
  const { data, description, traceHeader } = props

  const rootSpans = data.spans.filter((s) => s.parent_span_id === '')
  const [inputSpanName, inputField] = SplitField(description.inputAttribute)
  const inputSpan =
    inputSpanName === '' ? rootSpans[0] : data.spans.filter((s) => s.span_name === inputSpanName)[0]
  const [outputSpanName, outputField] = SplitField(description.outputAttribute)
  const lastSpan = rootSpans[rootSpans.length - 1]
  const outputSpan =
    outputSpanName === '' ? lastSpan : data.spans.filter((s) => s.span_name === outputSpanName)[0]
  const startTime = dayjs(data.start_time).locale('en-gb')
  const endTime = dayjs(data.end_time).locale('en-gb')

  return (
    <Stack gap={2} direction={'column'}>
      {traceHeader}

      <Message
        title={'User'}
        message={inputSpan ? inputSpan.attributes[inputField]?.toString() : '<undefined>'}
        align={'left'}
        time={startTime.isValid() ? startTime.format('ddd, MMM D, YYYY h:mm:ss A') : 'NaT'}
      />

      <Message
        title={'Assistant'}
        message={outputSpan ? outputSpan.attributes[outputField]?.toString() : '<undefined>'}
        time={endTime.isValid() ? endTime.format('ddd, MMM D, YYYY h:mm:ss A') : 'NaT'}
        align={'right'}
      />
    </Stack>
  )
}
