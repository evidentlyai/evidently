import type React from 'react'

import { Box, LinearProgress, Typography } from '@mui/material'

import type { PercentWidgetParams } from '~/api'

const ProgressWidgetContent: React.FunctionComponent<PercentWidgetParams> = (props) => (
  <div>
    <Box display='flex' alignItems='center'>
      <Box width='100%' mr={1}>
        <LinearProgress variant='determinate' value={(props.value / props.maxValue) * 100} />
      </Box>
      <Box minWidth={35}>
        <Typography variant='body2' color='textSecondary'>{`${Math.round(
          (props.value / props.maxValue) * 100
        )}%`}</Typography>
      </Box>
    </Box>
    <Box width='100%'>
      <Typography variant='body2' color='textSecondary'>
        {props.details ?? ''}
      </Typography>
    </Box>
  </div>
)

export default ProgressWidgetContent
