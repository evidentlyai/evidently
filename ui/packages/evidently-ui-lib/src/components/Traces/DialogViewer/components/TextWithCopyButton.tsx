import { ContentCopy } from '@mui/icons-material'
import { Box, IconButton } from '@mui/material'

export const TextWithCopyButton = ({ text }: { text: string | undefined }) => (
  <div style={{ display: 'flex', flexDirection: 'row-reverse' }}>
    <Box>
      <IconButton onClick={() => navigator.clipboard.writeText(text || '')}>
        <ContentCopy sx={{ fontSize: 20 }} />
      </IconButton>
    </Box>

    <span style={{ width: '100%', whiteSpace: 'pre-wrap' }}>{text}</span>
  </div>
)
