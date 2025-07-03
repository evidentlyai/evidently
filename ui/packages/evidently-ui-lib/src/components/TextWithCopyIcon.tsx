import ContentCopyIcon from '@mui/icons-material/ContentCopy'
import { IconButton, Tooltip } from '@mui/material'
import { Box } from '@mui/material'

export const TextWithCopyIcon = ({
  showText,
  copyText,
  tooltip
}: {
  showText: string
  copyText: string
  tooltip?: string
}) => {
  return (
    <Box>
      {showText}
      <Tooltip title={tooltip ?? 'Copy'} placement={'top'}>
        <IconButton
          size='small'
          style={{ marginLeft: 10 }}
          onClick={() => navigator.clipboard.writeText(copyText)}
        >
          <ContentCopyIcon fontSize='small' />
        </IconButton>
      </Tooltip>
    </Box>
  )
}
