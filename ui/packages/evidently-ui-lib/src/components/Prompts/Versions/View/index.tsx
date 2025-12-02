import { Stack } from '@mui/material'
import type { PromptTemplate, PromptVersionModel } from '~/api/types'
import { LLMJudgeTemplateViewer } from '~/components/Descriptors/Features/LLMJudge/template'
import { assertNever } from '~/utils'
import { Prompt } from './Prompt'

type ViewPromptVersionProps = {
  promptVersion: PromptVersionModel
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
}

export const ViewPromptVersion = (props: ViewPromptVersionProps) => {
  const { promptVersion, PromptViewerComponent } = props

  const { type } = promptVersion.content

  if (!type) {
    throw 'must provide type of prompt version'
  }

  if (type === 'evidently:prompt_content:TextPromptContent') {
    return <Prompt text={promptVersion.content.text} />
  }

  if (type === 'evidently:prompt_content:MessagesPromptContent') {
    return (
      <>
        <Stack direction={'column'} gap={4}>
          {promptVersion.content.messages.map((message) => (
            <Prompt key={message.content} text={message.content} role={message.role} />
          ))}
        </Stack>
      </>
    )
  }

  if (type === 'evidently:prompt_content:TemplatePromptContent') {
    return (
      <LLMJudgeTemplateViewer
        state={promptVersion.content.template}
        PromptViewerComponent={PromptViewerComponent}
      />
    )
  }

  assertNever(type)
}
