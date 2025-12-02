import { Chip, Stack, Typography } from '@mui/material'
import type { PromptVersionModel } from '~/api/types'
import { TextWithCopyIcon } from '~/components/Utils/TextWithCopyIcon'
import { type ModeType, ToggleViewEdit } from './ToggleViewEdit'

export type PromptInfoHeaderProps = {
  promptId: string
  promptVersion: PromptVersionModel
  mode: ModeType
  onModeChange: (newMode: ModeType) => void
}

export const PromptInfoHeader = (props: PromptInfoHeaderProps) => {
  const { promptId, promptVersion, mode, onModeChange } = props

  return (
    <Stack py={1} direction={'row'} gap={2}>
      <Stack direction={'row'} justifyContent={'flex-start'} alignItems={'center'} gap={1}>
        <Typography variant='body2'>Prompt ID</Typography>

        <Stack direction={'row'} justifyContent={'flex-start'} alignItems={'center'}>
          <Chip variant='filled' label={promptId} />
          <TextWithCopyIcon showText={''} copyText={promptId} />
        </Stack>
      </Stack>

      <Stack direction={'row'} justifyContent={'flex-start'} alignItems={'center'} gap={1}>
        <Typography>Version:</Typography>
        <Chip variant='outlined' size='small' label={`#${promptVersion.version}`} />
      </Stack>

      <Stack flex={1} direction={'row'} justifyContent={'flex-end'}>
        <ToggleViewEdit mode={mode} onModeChange={onModeChange} />
      </Stack>
    </Stack>
  )
}
