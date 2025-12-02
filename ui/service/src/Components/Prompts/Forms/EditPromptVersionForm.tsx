import type { LLMPromptTemplateModel, PromptTemplate } from 'evidently-ui-lib/api/types'
import { createContextForErrors } from 'evidently-ui-lib/components/FormHelpers/createContextForErrors'
import { useCustomFormValidator } from 'evidently-ui-lib/components/FormHelpers/hooks'
import {
  PromptVersionEditor,
  type PromptVersionErrorFields,
  type PromptVersionState,
  getPromptVersionErrors
} from 'evidently-ui-lib/components/Prompts/Versions/Edit/index'
import { Box, Button, Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'

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
