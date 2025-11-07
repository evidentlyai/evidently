import { RestartAlt as RestartAltIcon } from '@mui/icons-material'
import { Box, Button, Tooltip } from '@mui/material'

type ResetDatasetSettingsButtonProps = {
  isFilteringOrSorting?: boolean
  clearFiltersAndSortModel: () => void
}

export const ResetDatasetSettingsButton = (props: ResetDatasetSettingsButtonProps) => {
  const { isFilteringOrSorting, clearFiltersAndSortModel } = props

  return (
    <Box>
      <Tooltip title='Reset filtering and sorting settings'>
        <span>
          <Button
            size='small'
            variant='outlined'
            disabled={!isFilteringOrSorting}
            onClick={() => clearFiltersAndSortModel()}
            startIcon={<RestartAltIcon fontSize='inherit' />}
          >
            Reset
          </Button>
        </span>
      </Tooltip>
    </Box>
  )
}
