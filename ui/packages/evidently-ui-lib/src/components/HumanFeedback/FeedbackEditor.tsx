import {
  CheckCircleOutline as CheckCircleOutlineIcon,
  HelpOutline as HelpOutlineIcon,
  HighlightOff as HighlightOffIcon
} from '@mui/icons-material'
import { Box, Card, CardContent, Chip, Divider, Stack, TextField, Typography } from '@mui/material'
import { useEffect, useRef } from 'react'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { AddLabelPopover } from './AddLabelPopover'

export type FeedbackFormErrorFields = 'feedback' | 'label'

const { useErrors, createErrors } = createContextForErrors<FeedbackFormErrorFields>()

export type FeedbackData = {
  comment: string
  label: string
}

type FeedbackEditorProps = {
  feedbackData: FeedbackData
  setFeedbackData: (feedbackData: FeedbackData) => void
  additionalLabels: string[]
  setAdditionalLabels: (labels: string[]) => void
  additionalLabelsDisabled: boolean
  evaluationZero?: boolean
}

const LABEL_SHORTCUTS = [
  { label: 'pass', icon: <CheckCircleOutlineIcon fontSize='small' color='success' /> },
  { label: 'fail', icon: <HighlightOffIcon fontSize='small' color='error' /> },
  { label: 'unknown', icon: <HelpOutlineIcon fontSize='small' /> }
]

export const FeedbackEditor = (props: FeedbackEditorProps) => {
  const {
    feedbackData,
    setFeedbackData,
    additionalLabels,
    setAdditionalLabels,
    additionalLabelsDisabled,
    evaluationZero = false
  } = props

  const errors = useErrors()

  const ref = useRef<HTMLTextAreaElement>(null)

  const handleRemoveLabel = (labelToRemove: string) =>
    setAdditionalLabels(additionalLabels.filter((label) => label !== labelToRemove))

  useEffect(() => {
    if (ref.current) {
      ref.current.focus()

      // Position cursor at the end of the text
      const length = ref.current.value.length
      ref.current.setSelectionRange(length, length)
    }
  }, [])

  return (
    <Card {...(evaluationZero && { elevation: 0 })}>
      <CardContent>
        <Stack gap={2}>
          <Stack gap={1}>
            <Typography variant='h6'>Label</Typography>

            <TextField
              inputRef={ref}
              fullWidth
              value={feedbackData.label}
              onChange={(e) => setFeedbackData({ ...feedbackData, label: e.target.value })}
              placeholder='Enter label here...'
              variant='outlined'
              size='small'
              error={errors.label.isError}
              helperText={errors.label.errorMessage}
              sx={{ '& .MuiOutlinedInput-root': { fontFamily: 'monospace' } }}
            />

            <Box display='flex' gap={1} flexWrap='wrap'>
              {LABEL_SHORTCUTS.map(({ label, icon }) => (
                <Chip
                  key={label}
                  icon={icon}
                  label={label}
                  onClick={() => setFeedbackData({ ...feedbackData, label: label })}
                  variant={feedbackData.label === label ? 'filled' : 'outlined'}
                  sx={{ height: 35 }}
                />
              ))}
              {additionalLabels.length > 0 && <Divider flexItem orientation='vertical' />}

              {additionalLabels.map((label) => (
                <Chip
                  key={label}
                  label={label}
                  onClick={() => setFeedbackData({ ...feedbackData, label: label })}
                  onDelete={() => handleRemoveLabel(label)}
                  disabled={additionalLabelsDisabled}
                  variant={feedbackData.label === label ? 'filled' : 'outlined'}
                  sx={{ height: 35 }}
                />
              ))}
            </Box>

            <Box>
              <AddLabelPopover
                zeroEvaluation={evaluationZero}
                additionalLabelsDisabled={additionalLabelsDisabled}
                additionalLabels={additionalLabels}
                setAdditionalLabels={setAdditionalLabels}
              />
            </Box>

            <Divider sx={{ mt: 1 }} flexItem orientation='horizontal' />
          </Stack>

          <Stack gap={1}>
            <Typography variant='h6'>Feedback comment</Typography>

            <TextField
              fullWidth
              multiline
              value={feedbackData.comment}
              onChange={(e) => setFeedbackData({ ...feedbackData, comment: e.target.value })}
              placeholder='Enter your feedback here...'
              variant='outlined'
              error={errors.feedback.isError}
              helperText={errors.feedback.errorMessage}
              sx={{ '& .MuiOutlinedInput-root': { fontFamily: 'monospace' } }}
            />
          </Stack>
        </Stack>
      </CardContent>
    </Card>
  )
}

export const getFeedbackFormErrors = (state: FeedbackData) =>
  createErrors({
    label: {
      isError: !state.label.trim(),
      errorMessage: 'Provide a label'
    },
    feedback: { isError: false /* disable validation for feedback for now */, errorMessage: '' }
  })
