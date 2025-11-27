import { Box, Button, Stack } from '@mui/material'
import type { PromptTemplate, PromptVersionModel } from '~/api/types'
import { ViewPromptVersion } from '~/components/Prompts/Versions/View'

export type ViewPromptVersionFormProps = {
  promptVersion: PromptVersionModel
  PromptViewerComponent: (args: { data: PromptTemplate }) => JSX.Element
  onDeletePromptVersion: (promptVersionId: string) => void
  isDeleteDisabled: boolean
}

export const ViewPromptVersionForm = (props: ViewPromptVersionFormProps) => {
  const { promptVersion, PromptViewerComponent, onDeletePromptVersion, isDeleteDisabled } = props

  return (
    <Box>
      <ViewPromptVersion
        promptVersion={promptVersion}
        PromptViewerComponent={PromptViewerComponent}
      />

      <Stack mt={2} direction={'row'} justifyContent={'flex-end'}>
        <Button
          variant='outlined'
          onClick={() => onDeletePromptVersion(promptVersion.id ?? '')}
          disabled={isDeleteDisabled}
        >
          Delete this version
        </Button>
      </Stack>
    </Box>
  )
}
