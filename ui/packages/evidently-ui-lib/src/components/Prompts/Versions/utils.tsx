import type { PromptVersionModel } from '~/api/types'
import { assertNever } from '~/utils'
import type { PromptVersionState } from './Edit'

type PromptVersion2EditStateArgs = {
  promptVersion: PromptVersionModel | null | undefined
}

export const promptVersion2EditState = (args: PromptVersion2EditStateArgs): PromptVersionState => {
  const { promptVersion } = args

  if (!promptVersion) {
    return {
      variant: 'text',
      messagesState: { messages: [{ id: 'default', role: 'user' as const, text: '' }] }
    }
  }

  if (promptVersion?.content.type === 'evidently:prompt_content:TextPromptContent') {
    return {
      variant: 'text',
      messagesState: {
        messages: [
          { id: 'default', role: 'user' as const, text: promptVersion?.content.text ?? '' }
        ]
      }
    }
  }

  if (promptVersion?.content.type === 'evidently:prompt_content:MessagesPromptContent') {
    return {
      variant: 'messages',
      messagesState: {
        messages: (promptVersion?.content.messages ?? []).map((message, index) => ({
          id: String(index),
          role: message.role as 'user' | 'system',
          text: message.content
        }))
      }
    }
  }

  if (promptVersion?.content.type === 'evidently:prompt_content:TemplatePromptContent') {
    return {
      variant: 'llm_judge',
      llmJudgeTemplateState: promptVersion.content.template
    }
  }

  if (
    !promptVersion?.content.type ||
    promptVersion?.content.type === 'evidently:prompt_content:JudgePromptContent'
  ) {
    throw 'unsupported JudgePromptContent here'
  }

  assertNever(promptVersion?.content.type)
}

type EditState2PromptVersionArgs = {
  editState: PromptVersionState
}

export const editState2PromptVersion = (
  args: EditState2PromptVersionArgs
): Omit<PromptVersionModel, 'version'> => {
  const { editState } = args

  if (editState.variant === 'text') {
    return {
      content_type: editState.variant,
      content: {
        type: 'evidently:prompt_content:TextPromptContent',
        text: editState.messagesState.messages.at(0)?.text ?? ''
      }
    }
  }

  if (editState.variant === 'messages') {
    return {
      content_type: editState.variant,
      content: {
        type: 'evidently:prompt_content:MessagesPromptContent',
        messages: editState.messagesState.messages.map((m) => ({
          content: m.text,
          role: m.role
        }))
      }
    }
  }

  if (editState.variant === 'llm_judge') {
    return {
      content_type: 'template',
      content: {
        type: 'evidently:prompt_content:TemplatePromptContent',
        template: editState.llmJudgeTemplateState
      }
    }
  }

  assertNever(editState.variant)
}
