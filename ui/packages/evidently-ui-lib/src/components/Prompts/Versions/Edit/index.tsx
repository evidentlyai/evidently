import { Box, Button, Stack, Typography } from '@mui/material'
import { useState } from 'react'
import type { LLMPromptTemplateModel, PromptTemplate } from '~/api/types'
import { BinaryTemplateSelector } from '~/components/Descriptors/Features/LLMJudge/BinaryTemplateChips'
import {
  LLMJudgeTemplateEditor,
  type TemplateErrorFields,
  getLLMJudgeTemplateErrors
} from '~/components/Descriptors/Features/LLMJudge/template'
import { createContextForErrors } from '~/components/FormHelpers/createContextForErrors'
import { useCustomFormValidator } from '~/components/FormHelpers/hooks'
import { useDebounce } from '~/hooks'
import { assertNever } from '~/utils'
import { EditPromptVersionMessages, getMessagesErrors } from './impls'
import type { MessagesErrorFields, MessagesPromptVersionState } from './impls'

export type PromptVersionErrorFields = MessagesErrorFields | TemplateErrorFields
const { WithErrors, createErrors, isValid } = createContextForErrors<PromptVersionErrorFields>()

export type PromptVersionState =
  | {
      variant: 'text' | 'messages'
      messagesState: MessagesPromptVersionState
    }
  | {
      variant: 'llm_judge'
      llmJudgeTemplateState: PromptTemplate
    }

type PromptVersionEditorProps = {
  state: PromptVersionState
  setState: React.Dispatch<React.SetStateAction<PromptVersionState>>
  prompts: LLMPromptTemplateModel[]
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

export const PromptVersionEditor = (props: PromptVersionEditorProps) => {
  const { state, setState, prompts, PromptViewerComponent } = props

  if (state.variant === 'text' && state.messagesState.messages.length > 1) {
    setState({ ...state, variant: 'messages' })
  }

  if (state.variant === 'messages' && state.messagesState.messages.length === 1) {
    setState({ ...state, variant: 'text' })
  }

  if (state.variant === 'text' || state.variant === 'messages') {
    return (
      <EditPromptVersionMessages
        state={state.messagesState}
        setState={(stateAction) =>
          setState({
            ...state,
            messagesState:
              typeof stateAction === 'function' ? stateAction(state.messagesState) : stateAction
          })
        }
      />
    )
  }

  if (state.variant === 'llm_judge') {
    return (
      <EditLLMJudgePromptVersion
        state={state}
        setState={setState}
        prompts={prompts}
        PromptViewerComponent={PromptViewerComponent}
      />
    )
  }

  assertNever(state.variant)
}

type EditLLMJudgePromptVersionProps = {
  state: Extract<PromptVersionState, { variant: 'llm_judge' }>
  setState: React.Dispatch<React.SetStateAction<PromptVersionState>>
  prompts: LLMPromptTemplateModel[]
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

const EditLLMJudgePromptVersion = (props: EditLLMJudgePromptVersionProps) => {
  const { state, setState, prompts, PromptViewerComponent } = props

  const templateDebounced = useDebounce(state, 300)

  return (
    <Stack gap={2}>
      <BinaryTemplateSelector
        prompts={prompts}
        onChangeBinaryTemplate={(template) => {
          setState({
            ...state,
            llmJudgeTemplateState: template
          })
        }}
      />

      <LLMJudgeTemplateEditor
        state={state.llmJudgeTemplateState}
        setState={(stateAction) =>
          setState({
            ...state,
            llmJudgeTemplateState:
              typeof stateAction === 'function'
                ? stateAction(state.llmJudgeTemplateState)
                : stateAction
          })
        }
      />

      <Stack alignItems={'flex-start'}>
        <PromptViewerComponent data={templateDebounced.llmJudgeTemplateState} />
      </Stack>
    </Stack>
  )
}

type PromptVersionFormProps = {
  defaultValues: PromptVersionState
  onSuccess: (state: PromptVersionState) => void
  buttonTitle: string
  prompts: LLMPromptTemplateModel[]
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

export const PromptVersionForm = (props: PromptVersionFormProps) => {
  const { defaultValues, onSuccess, buttonTitle, prompts, PromptViewerComponent } = props

  const [state, setState] = useState(defaultValues)

  const errors = getPromptVersionErrors(state)

  const { submitButtonProps, showErrors } = useCustomFormValidator({
    isStateValid: isValid(errors),
    onSubmitWithValidState: () => onSuccess(state)
  })

  return (
    <Box>
      <Typography fontWeight={600} align='center' variant='h4' gutterBottom mb={4}>
        Create prompt version
      </Typography>

      <WithErrors errors={errors} showErrors={showErrors}>
        <PromptVersionEditor
          state={state}
          setState={setState}
          prompts={prompts}
          PromptViewerComponent={PromptViewerComponent}
        />
      </WithErrors>

      <Stack mt={2} direction={'row'} justifyContent={'flex-end'}>
        <Button {...submitButtonProps} variant='contained'>
          {buttonTitle}
        </Button>
      </Stack>
    </Box>
  )
}

export const getPromptVersionErrors = (state: PromptVersionState) => {
  if (state.variant === 'llm_judge') {
    return getLLMJudgeTemplateErrors(state.llmJudgeTemplateState) as ReturnType<typeof createErrors>
  }

  if (state.variant === 'messages' || state.variant === 'text') {
    return getMessagesErrors(state.messagesState) as ReturnType<typeof createErrors>
  }

  assertNever(state.variant)
}
