import { Stack, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material'

export type ModeType = 'view' | 'edit'

type ToggleViewEditProps = {
  mode: ModeType
  onModeChange: (newMode: ModeType) => void
}

export const ToggleViewEdit = (props: ToggleViewEditProps) => {
  const { mode, onModeChange } = props

  return (
    <>
      <Stack direction={'row'} alignItems={'center'} gap={1}>
        <Typography>Mode</Typography>

        <ToggleButtonGroup
          size='small'
          value={mode}
          exclusive
          onChange={(_, value) => {
            if (value) {
              onModeChange(value)
            }
          }}
        >
          {(['view', 'edit'] satisfies ModeType[]).map((value) => (
            <ToggleButton key={value} value={value} sx={{ textTransform: 'capitalize' }}>
              {value}
            </ToggleButton>
          ))}
        </ToggleButtonGroup>
      </Stack>
    </>
  )
}
