import RefreshIcon from '@mui/icons-material/Refresh'
import { Box, IconButton, Tooltip } from '@mui/material'
import { useFetcher } from 'react-router-dom'

export const ReloadAllButton = ({
  tooltipTitle,
  action
}: { tooltipTitle: string; action: string }) => {
  const fetcher = useFetcher()
  return (
    <Box>
      <Tooltip title={tooltipTitle}>
        <IconButton
          disabled={fetcher.state !== 'idle'}
          onClick={() =>
            fetcher.submit(null, {
              action,
              encType: 'application/json',
              method: 'POST',
              preventScrollReset: true
            })
          }
        >
          <RefreshIcon />
        </IconButton>
      </Tooltip>
    </Box>
  )
}
