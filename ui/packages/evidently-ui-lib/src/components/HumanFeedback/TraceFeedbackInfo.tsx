import { Feedback as FeedbackIcon } from '@mui/icons-material'
import { Button, Chip, Stack, Typography } from '@mui/material'

export type TraceFeedbackInfoProps = {
  label: string
  comment: string
  onEdit: () => void
  isEditing: boolean
}

export const TraceFeedbackInfo = (props: TraceFeedbackInfoProps) => {
  const { label, comment, onEdit, isEditing } = props

  const hasFeedback = Boolean(label || comment)

  return (
    <Stack direction='row' gap={1} alignItems='center'>
      {hasFeedback && (
        <Stack direction='row' gap={1} alignItems='center'>
          {label && <Chip label={label} size='small' variant='outlined' />}
          {comment && (
            <Typography
              title={comment}
              variant='caption'
              color='text.secondary'
              sx={{
                maxWidth: 200,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
              }}
            >
              {comment}
            </Typography>
          )}
        </Stack>
      )}

      <Button size='small' variant='outlined' startIcon={<FeedbackIcon />} onClick={onEdit}>
        Edit feedback
      </Button>

      {isEditing && <Chip label='Editing' size='small' color='primary' variant='filled' />}
    </Stack>
  )
}
