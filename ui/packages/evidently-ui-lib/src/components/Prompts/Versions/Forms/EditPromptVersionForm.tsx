import { Box, Button, Stack } from '@mui/material'
import { useState } from 'react'
import type { LLMPromptTemplateModel, PromptTemplate } from '~/api/types'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { useCustomFormValidator } from '~/components/FormHelpers/hooks'
import {
  PromptVersionEditor,
  type PromptVersionErrorFields,
  type PromptVersionState,
  getPromptVersionErrors
} from '~/components/Prompts/Versions/Edit'

const PromptVersionHelpers = createContextForErrors<PromptVersionErrorFields>()

export type EditPromptVersionFormProps = {
  defaultValues: PromptVersionState
  prompts: LLMPromptTemplateModel[]
  onSaveAsNewVersion: (state: PromptVersionState) => void
  saveAsNewVersionDisabled: boolean
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

export const EditPromptVersionForm = (props: EditPromptVersionFormProps) => {
  const {
    defaultValues,
    onSaveAsNewVersion,
    prompts,
    saveAsNewVersionDisabled,
    PromptViewerComponent
  } = props

  const [state, setState] = useState(defaultValues)
  const promptVersionErrors = getPromptVersionErrors(state)

  const promptVersionValidator = useCustomFormValidator({
    isStateValid: PromptVersionHelpers.isValid(promptVersionErrors),
    onSubmitWithValidState: () => onSaveAsNewVersion(state)
  })

  return (
    <Box>
      <PromptVersionHelpers.WithErrors
        errors={promptVersionErrors}
        showErrors={promptVersionValidator.showErrors}
      >
        <PromptVersionEditor
          state={state}
          setState={setState}
          prompts={prompts}
          PromptViewerComponent={PromptViewerComponent}
        />
      </PromptVersionHelpers.WithErrors>

      <Stack mt={2} direction={'row'} justifyContent={'flex-end'}>
        <Button
          {...promptVersionValidator.submitButtonProps}
          disabled={promptVersionValidator.submitButtonProps.disabled || saveAsNewVersionDisabled}
          variant='contained'
        >
          Save as new version
        </Button>
      </Stack>
    </Box>
  )
}
