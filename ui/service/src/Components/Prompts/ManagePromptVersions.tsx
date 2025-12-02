import type { PromptVersionModel } from 'evidently-ui-lib/api/types'
import { PromptInfoHeader } from 'evidently-ui-lib/components/Prompts/PromptInfoHeader'
import { PromptVersionsSidebar } from 'evidently-ui-lib/components/Prompts/PromptVersionsSidebar'
import type { ModeType } from 'evidently-ui-lib/components/Prompts/ToggleViewEdit'
import { promptVersion2EditState } from 'evidently-ui-lib/components/Prompts/Versions/utils'
import { Box, Stack, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type React from 'react'
import { useMemo } from 'react'
import {
  EditPromptVersionForm,
  type EditPromptVersionFormProps
} from './Forms/EditPromptVersionForm'
import {
  ViewPromptVersionForm,
  type ViewPromptVersionFormProps
} from './Forms/ViewPromptVersionForm'

export type ManagePromptVersionsProps = {
  promptId: string
  latestPromptVersion: PromptVersionModel | null
  promptVersions: PromptVersionModel[]
  selectedPromptVersionId: string | null
  onChangeSelectedPromptVersionId: (promptId: string) => void
  mode: ModeType
  onModeChange: (newMode: ModeType) => void
  createNewVersionButton: React.ReactNode
  createFirstVersionButton: React.ReactNode
  editPromptVersionProps: Omit<EditPromptVersionFormProps, 'defaultValues'>
  viewPromptVersionProps: Omit<ViewPromptVersionFormProps, 'promptVersion'>
}

export const ManagePromptVersions = (props: ManagePromptVersionsProps) => {
  const {
    latestPromptVersion,
    promptVersions: promptVersionsRaw,
    promptId,
    mode,
    onModeChange,
    selectedPromptVersionId,
    onChangeSelectedPromptVersionId,
    editPromptVersionProps,
    viewPromptVersionProps,
    createNewVersionButton,
    createFirstVersionButton
  } = props

  const promptVersions = useMemo(
    () => promptVersionsRaw.toSorted((a, b) => b.version - a.version),
    [promptVersionsRaw]
  )

  const promptVersion = promptVersions.find((p) => p.id === selectedPromptVersionId)

  return (
    <>
      {promptVersions.length === 0 && (
        <Stack direction={'column'} gap={1} alignItems={'center'} justifyContent={'center'}>
          <Typography mt={3} variant='h4' align='center' gutterBottom>
            You don't have any versions yet.
          </Typography>

          {createFirstVersionButton}
        </Stack>
      )}

      {promptVersion && (
        <Box
          mt={5}
          display={'grid'}
          gridTemplateColumns={`${20}% calc(100% - ${20}%)`}
          alignItems={'start'}
          sx={{ transition: '625ms ease-in-out', minHeight: 'calc(100vh - 350px)' }}
        >
          <PromptVersionsSidebar
            promptVersions={promptVersions}
            latestPromptVersion={latestPromptVersion}
            selectedPromptVersionId={selectedPromptVersionId}
            onChangeSelectedPromptVersionId={onChangeSelectedPromptVersionId}
            createNewVersionButton={createNewVersionButton}
          />

          <Box position={'sticky'} top={20} left={0}>
            <Box sx={{ minWidth: 400, mx: 'auto', mt: 1, width: 0.9 }}>
              <PromptInfoHeader
                promptId={promptId}
                promptVersion={promptVersion}
                mode={mode}
                onModeChange={onModeChange}
              />

              <Box mt={2}>
                {mode === 'view' && (
                  <ViewPromptVersionForm
                    promptVersion={promptVersion}
                    {...viewPromptVersionProps}
                  />
                )}

                {mode === 'edit' && (
                  <EditPromptVersionForm
                    // key is essential to clear internal state when prompt version changes
                    key={promptVersion.id ?? ''}
                    defaultValues={promptVersion2EditState({ promptVersion })}
                    {...editPromptVersionProps}
                  />
                )}
              </Box>
            </Box>
          </Box>
        </Box>
      )}
    </>
  )
}
