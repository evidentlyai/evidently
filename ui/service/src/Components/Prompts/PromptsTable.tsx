import type { PromptModel } from 'evidently-ui-lib/api/types'
import { PromptsTable as PromptsTableLib } from 'evidently-ui-lib/components/Prompts/PromptsTable'
import { Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'

type PromptsTableProps = {
  prompts: PromptModel[]
  isLoading: boolean
  onDelete: (promptId: string) => void
  GetPromptLinkByID: (args: { promptId: string }) => JSX.Element
  createNewPromptButton: React.ReactNode
  createFirstPromptButton: React.ReactNode
}

export const PromptsTable = (props: PromptsTableProps) => {
  const {
    prompts,
    isLoading,
    onDelete,
    GetPromptLinkByID,
    createNewPromptButton,
    createFirstPromptButton
  } = props

  const isPromptsEmpty = prompts.length === 0

  return (
    <>
      {!isPromptsEmpty && (
        <Stack my={1} direction={'row'} alignItems={'center'}>
          {createNewPromptButton}
        </Stack>
      )}

      <PromptsTableLib
        isLoading={isLoading}
        onDelete={onDelete}
        GetPromptLinkByID={GetPromptLinkByID}
        prompts={prompts}
      />

      {isPromptsEmpty && (
        <Stack direction={'row'} alignItems={'center'} justifyContent={'center'}>
          {createFirstPromptButton}
        </Stack>
      )}
    </>
  )
}
