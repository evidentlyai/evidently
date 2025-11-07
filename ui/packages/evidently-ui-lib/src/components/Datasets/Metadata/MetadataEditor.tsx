import { Delete as DeleteIcon } from '@mui/icons-material'
import { Box, IconButton, Stack, TextField } from '@mui/material'

export type MetadataItem = {
  key: string
  value: string
}

export type MetadataEditorProps = {
  items: MetadataItem[]
  onMetadataChange: (metadata: MetadataItem[]) => void
}

export const MetadataEditor = (props: MetadataEditorProps) => {
  const { items, onMetadataChange } = props

  return (
    <>
      {items.map((it, idx) => (
        /*biome-ignore lint/suspicious/noArrayIndexKey: fine*/
        <Stack key={`m${idx}`} direction={'row'} spacing={2}>
          <TextField
            size={'small'}
            label={'key'}
            value={it.key}
            onChange={(value) => {
              const newItems = [...items]
              newItems[idx].key = value.target.value
              onMetadataChange(newItems)
            }}
          />
          <TextField
            size={'small'}
            label={'value'}
            value={it.value}
            onChange={(value) => {
              const newItems = [...items]
              newItems[idx].value = value.target.value
              onMetadataChange(newItems)
            }}
          />
          <Box>
            <IconButton onClick={() => onMetadataChange(items.filter((_, i) => i !== idx))}>
              <DeleteIcon fontSize='small' />
            </IconButton>
          </Box>
        </Stack>
      ))}
    </>
  )
}
