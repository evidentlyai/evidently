import { ContentCopy } from '@mui/icons-material'
import { Box, IconButton, Stack, Typography } from '@mui/material'

export const TextWithCopyButton = ({ text }: { text: string | undefined }) => {
  return (
    <Stack direction={'row'} justifyContent={'flex-end'}>
      <Stack direction={'row'} justifyContent={'center'} gap={1} alignItems={'center'}>
        <Typography>{text}</Typography>
        <Box>
          <IconButton onClick={() => navigator.clipboard.writeText(text ?? '')}>
            <ContentCopy sx={{ fontSize: 20 }} />
          </IconButton>
        </Box>
      </Stack>
    </Stack>
  )
}
