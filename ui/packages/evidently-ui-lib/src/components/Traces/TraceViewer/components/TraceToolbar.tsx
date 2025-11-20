import { ArrowBack as ArrowBackIcon } from '@mui/icons-material'
import { ArrowForward as ArrowForwardIcon } from '@mui/icons-material'
import { Autocomplete, Box, Button, IconButton, Stack, TextField, Tooltip } from '@mui/material'

type TraceToolbarProps = {
  traceId: string
  traceIds: string[]
  onBackToTableView: () => void
  onSelectTrace: (traceId: string) => void
  goToNextTrace: () => void
  goToPreviousTrace: () => void
  isPossibleToGoToNextTrace: boolean
  isPossibleToGoToPreviousTrace: boolean
}

export const TraceToolbar = (props: TraceToolbarProps) => {
  const {
    traceId,
    traceIds,
    onBackToTableView,
    onSelectTrace,
    goToNextTrace,
    goToPreviousTrace,
    isPossibleToGoToNextTrace,
    isPossibleToGoToPreviousTrace
  } = props

  return (
    <Stack py={2} direction={'row'} gap={2} alignItems={'center'}>
      <Button variant='contained' startIcon={<ArrowBackIcon />} onClick={() => onBackToTableView()}>
        Go to table view
      </Button>
      <Box width={410}>
        <Autocomplete
          size='small'
          value={traceId}
          onChange={(_, value) => value && onSelectTrace(value)}
          options={traceIds}
          renderInput={(params) => <TextField label={'Trace'} {...params} />}
        />
      </Box>

      <Tooltip title='Previous trace' placement='top'>
        <span>
          <IconButton
            disabled={!isPossibleToGoToPreviousTrace}
            onClick={() => goToPreviousTrace()}
            size='small'
          >
            <ArrowBackIcon />
          </IconButton>
        </span>
      </Tooltip>

      <Tooltip title='Next trace' placement='top'>
        <span>
          <IconButton
            disabled={!isPossibleToGoToNextTrace}
            onClick={() => goToNextTrace()}
            size='small'
          >
            <ArrowForwardIcon />
          </IconButton>
        </span>
      </Tooltip>
    </Stack>
  )
}
