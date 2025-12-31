import { ContentCopy as ContentCopyIcon } from '@mui/icons-material'
import { Box, Chip, IconButton, Stack, Tooltip, Typography } from '@mui/material'
import type React from 'react'
import {
  TraceFeedbackInfo,
  type TraceFeedbackInfoProps
} from '~/components/HumanFeedback/TraceFeedbackInfo'

export type TraceHeaderProps = {
  traceId: string
  feedback: TraceFeedbackInfoProps
  additionalComponents?: React.ReactNode
}

export const TraceHeader = (props: TraceHeaderProps) => {
  const { traceId, feedback, additionalComponents } = props

  return (
    <Stack direction='row' gap={2} alignItems='center' justifyContent='space-between'>
      <Stack
        direction={'row'}
        justifyContent={'flex-start'}
        alignItems={'center'}
        gap={1}
        flexWrap='wrap'
      >
        <TraceIdDisplay traceId={traceId} />

        <TraceFeedbackInfo {...feedback} />
      </Stack>

      <Box minWidth={'fit-content'}>{additionalComponents}</Box>
    </Stack>
  )
}

export const TraceIdDisplay = ({ traceId }: { traceId: string }) => (
  <Stack direction={'row'} alignItems={'center'}>
    <Typography mr={1} variant='body2'>
      Trace ID
    </Typography>

    <Chip variant='filled' label={traceId} size='small' />
    <Tooltip title={'Copy'} placement={'top'}>
      <IconButton size='small' onClick={() => navigator.clipboard.writeText(traceId)}>
        <ContentCopyIcon fontSize='small' />
      </IconButton>
    </Tooltip>
  </Stack>
)
