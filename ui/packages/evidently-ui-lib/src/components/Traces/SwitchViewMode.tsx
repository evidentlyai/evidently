import { Stack, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material'

export type TraceViewVariant = 'trace' | 'dataset' | 'dialog'

type SwitchViewModeProps = {
  value: TraceViewVariant
  onChange: (view: TraceViewVariant) => void
  isLoading: boolean
}

export const SwitchViewMode = (props: SwitchViewModeProps) => {
  const { value, onChange, isLoading } = props

  return (
    <Stack direction={'row'} alignItems={'center'} gap={1} sx={[isLoading && { opacity: 0.6 }]}>
      <Typography variant={'button'}>View mode</Typography>

      <ToggleButtonGroup
        size='small'
        value={value}
        exclusive
        onChange={(_, value) => {
          if (value) {
            onChange(value)
          }
        }}
      >
        {(['trace', 'dataset', 'dialog'] satisfies TraceViewVariant[]).map((value) => (
          <ToggleButton key={value} value={value} sx={{ textTransform: 'capitalize' }}>
            {value}
          </ToggleButton>
        ))}
      </ToggleButtonGroup>
    </Stack>
  )
}
