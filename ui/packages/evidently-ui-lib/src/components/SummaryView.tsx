import type React from 'react'

import { Box, Button, Grid, Select } from '@mui/material'

import type { DashboardInfoModel } from '~/api/types'
import { DashboardContentWidgets } from './DashboardContent'

interface SummaryViewProps {
  dashboardInfo: DashboardInfoModel
}

const SummaryView: React.FunctionComponent<SummaryViewProps> = (props) => {
  return (
    <Box mt={10} flexGrow={1}>
      <Grid container spacing={3} direction='row' alignItems='stretch'>
        <Grid item xs={12} sx={{ display: 'flex', verticalAlign: 'baseline' }}>
          <Select
            variant='standard'
            label='Age'
            labelId='time_range_label'
            value={'recent'}
            inputProps={{
              name: 'age',
              id: 'age-native-simple'
            }}
          >
            <option value={'6m'}>Last 6 months</option>
            <option value={'3m'}>Last 3 months</option>
            <option value={'recent'}>Recent data</option>
          </Select>
          <Box flexGrow={1} />
          <Box>
            <Button sx={{ ml: 1 }} variant={'contained'} color='primary'>
              Edit
            </Button>
            <Button sx={{ ml: 1 }} variant={'contained'} color='primary'>
              Export
            </Button>
          </Box>
        </Grid>
        <DashboardContentWidgets widgets={props.dashboardInfo.widgets} />
      </Grid>
    </Box>
  )
}

export default SummaryView
