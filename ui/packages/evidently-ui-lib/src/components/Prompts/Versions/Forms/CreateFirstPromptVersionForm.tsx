import { Box, Button, Stack, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material'
import type { LLMPromptTemplateModel, PromptTemplate } from '~/api/types'
import { makeEmptyLLMJudgeDescriptorTemplate } from '~/components/Descriptors/_utils/utils'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { useCustomFormValidator } from '~/components/FormHelpers/hooks'
import {
  PromptVersionEditor,
  type PromptVersionErrorFields,
  type PromptVersionState,
  getPromptVersionErrors
} from '~/components/Prompts/Versions/Edit'

import { useState } from 'react'
import { assertNever } from '~/utils'

const { WithErrors, isValid } = createContextForErrors<PromptVersionErrorFields>()

type VariantType = 'text-messages' | 'judge'

type CreateFirstPromptVersionFormProps = {
  onSuccess: (data: PromptVersionState) => void
  defaultValues: PromptVersionState
  prompts: LLMPromptTemplateModel[]
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
  isLoading: boolean
}

export const CreateFirstPromptVersionForm = (props: CreateFirstPromptVersionFormProps) => {
  const { defaultValues, onSuccess, prompts, PromptViewerComponent, isLoading } = props
  const [state, setState] = useState(defaultValues)

  const errors = getPromptVersionErrors(state)

  const { submitButtonProps, showErrors } = useCustomFormValidator({
    isStateValid: isValid(errors),
    onSubmitWithValidState: () => onSuccess(state)
  })

  const [variant, setVariant] = useState<VariantType>('text-messages')

  return (
    <Box>
      <Typography fontWeight={600} align='center' variant='h4' gutterBottom mb={4}>
        Create your first prompt version
      </Typography>

      <PromptVariantToggle
        variant={variant}
        onChange={(variant) => {
          setVariant(variant)

          if (variant === 'text-messages') {
            setState({
              variant: 'text',
              messagesState: { messages: [{ id: 'default', role: 'user', text: '' }] }
            })
            return
          }

          if (variant === 'judge') {
            setState({
              variant: 'llm_judge',
              llmJudgeTemplateState: makeEmptyLLMJudgeDescriptorTemplate()
            })
            return
          }

          assertNever(variant)
        }}
      />

      <Box>
        <WithErrors errors={errors} showErrors={showErrors}>
          <PromptVersionEditor
            state={state}
            setState={setState}
            prompts={prompts}
            PromptViewerComponent={PromptViewerComponent}
          />
        </WithErrors>

        <Stack mt={2} direction={'row'} justifyContent={'flex-end'}>
          <Button
            onClick={submitButtonProps.onClick}
            disabled={isLoading || submitButtonProps.disabled}
            variant='contained'
          >
            Save
          </Button>
        </Stack>
      </Box>
    </Box>
  )
}

type PromptVariantToggleProps = {
  variant: VariantType
  onChange: (value: VariantType) => void
}

const PromptVariantToggle = (props: PromptVariantToggleProps) => {
  const { variant, onChange } = props

  return (
    <Box display='flex' justifyContent='center' my={2}>
      <ToggleButtonGroup
        size='small'
        value={variant}
        exclusive
        onChange={(_, value) => {
          if (!value) {
            return
          }

          onChange(value as VariantType)
        }}
      >
        {(
          [
            ['text-messages', 'free form'],
            ['judge', 'LLM Judge']
          ] satisfies [VariantType, string][]
        ).map(([value, label]) => (
          <ToggleButton key={value} value={value} sx={{ textTransform: 'capitalize' }}>
            {label}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Box>
  )
}
