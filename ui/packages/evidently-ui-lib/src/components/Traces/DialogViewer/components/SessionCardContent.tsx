import { Divider, Typography } from '@mui/material'
import type { TraceModel } from 'api/types'
import { SplitField } from '../helpers'
import type { Description } from '../types'

type SessionCardContentProps = {
  traces: TraceModel[]
  description: Description
}
export const SessionCardContent = (props: SessionCardContentProps) => {
  const { traces, description } = props

  const data = traces[0]
  const rootSpans = data.spans.filter((s) => s.parent_span_id === '')
  const [inputSpanName, inputField] = SplitField(description.inputAttribute)
  const inputSpan =
    inputSpanName === '' ? rootSpans[0] : data.spans.filter((s) => s.span_name === inputSpanName)[0]
  const [outputSpanName, outputField] = SplitField(description.outputAttribute)
  const lastSpan = rootSpans[rootSpans.length - 1]

  const outputSpan =
    outputSpanName === '' ? lastSpan : data.spans.filter((s) => s.span_name === outputSpanName)[0]

  const userMessage = inputSpan.attributes[inputField]?.toString()

  const agentMessage = outputSpan.attributes[outputField]?.toString()

  return (
    <>
      <Typography
        variant={'subtitle2'}
        component='pre'
        sx={{ fontFamily: 'monospace', whiteSpace: 'break-spaces' }}
      >
        <b>User</b>: {userMessage?.length > 30 ? `${userMessage?.slice(0, 30)}...` : userMessage}
        <br />
        <b>Agent</b>:{' '}
        {agentMessage?.length > 30 ? `${agentMessage?.slice(0, 30)}...` : agentMessage}
      </Typography>
      <Divider sx={{ my: 1 }} />
      <Typography variant='subtitle2'>{traces.length * 2} messages</Typography>
    </>
  )
}
