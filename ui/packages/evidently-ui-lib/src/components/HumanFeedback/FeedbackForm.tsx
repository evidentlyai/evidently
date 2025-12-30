import { Button, Stack } from '@mui/material'
import type React from 'react'
import { useEffect, useState } from 'react'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { useCustomFormValidator } from '~/components/FormHelpers/hooks'
import { useStableCallbackWithLatestScope } from '~/hooks/index'
import {
  type FeedbackData,
  FeedbackEditor,
  type FeedbackFormErrorFields,
  getFeedbackFormErrors
} from './FeedbackEditor'

const { WithErrors, isValid } = createContextForErrors<FeedbackFormErrorFields>()

type FeedbackFormProps = {
  defaultFeedbackData: FeedbackData
  onSubmitFeedbackData: (feedbackData: FeedbackData) => void
  submitDisabled: boolean
  leftButtons?: React.ReactNode
  additionalLabels: string[]
  setAdditionalLabels: (labels: string[]) => void
  additionalLabelsDisabled: boolean
  evaluationZero?: boolean
  buttonText?: string
}

export const FeedbackForm = (props: FeedbackFormProps) => {
  const {
    defaultFeedbackData,
    onSubmitFeedbackData,
    submitDisabled,
    leftButtons,
    additionalLabels,
    setAdditionalLabels,
    additionalLabelsDisabled,
    buttonText = 'Save & Next',
    evaluationZero = false
  } = props

  const [feedbackData, setFeedbackData] = useState(defaultFeedbackData)

  const isTouched = !(
    defaultFeedbackData.comment === feedbackData.comment &&
    defaultFeedbackData.label === feedbackData.label
  )

  const errors = getFeedbackFormErrors(feedbackData)

  const validator = useCustomFormValidator({
    isStateValid: isValid(errors),
    onSubmitWithValidState: () => onSubmitFeedbackData(feedbackData)
  })

  const disabled = !isTouched || submitDisabled || validator.submitButtonProps.disabled

  const handleKeyDown = useStableCallbackWithLatestScope((e: KeyboardEvent) => {
    // Global keyboard handler for Ctrl/Cmd+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && !disabled) {
      e.preventDefault()
      validator.submitButtonProps.onClick()
    }
  })

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    // Global keyboard handler for Ctrl/Cmd+Enter

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <WithErrors errors={errors} showErrors={validator.showErrors}>
      <Stack direction='column' gap={2}>
        <FeedbackEditor
          feedbackData={feedbackData}
          setFeedbackData={setFeedbackData}
          additionalLabels={additionalLabels}
          setAdditionalLabels={setAdditionalLabels}
          additionalLabelsDisabled={additionalLabelsDisabled}
          evaluationZero={evaluationZero}
        />

        <Stack direction='row' gap={2} justifyContent='space-between'>
          {leftButtons}

          <Button
            variant='contained'
            disabled={disabled}
            onClick={validator.submitButtonProps.onClick}
            endIcon={<span style={{ opacity: 0.8, fontSize: '0.875rem' }}>⌘↵</span>}
          >
            {buttonText}
          </Button>
        </Stack>
      </Stack>
    </WithErrors>
  )
}
