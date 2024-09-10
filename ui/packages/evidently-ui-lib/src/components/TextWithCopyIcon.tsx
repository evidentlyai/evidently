import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { IconButton } from '@mui/material'
import { Box } from '@mui/material'

export const TextWithCopyIcon = ({
  showText,
  copyText
}: {
  showText: string
  copyText: string
}) => {
  return (
    <Box>
      {showText}
      <IconButton
        size='small'
        style={{ marginLeft: 10 }}
        onClick={() => navigator.clipboard.writeText(copyText)}
      >
        <ContentCopyIcon fontSize='small' />
      </IconButton>
    </Box>
  )
}
