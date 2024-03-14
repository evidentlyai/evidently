import React from 'react'
import { Box, Grid, Typography } from '@mui/material'
import { CounterInfo } from '~/api'

interface CounterWidgetProps {
  counters: CounterInfo[]
}

const CounterItem: React.FunctionComponent<CounterInfo> = (props) => (
  <div>
    <Typography fontWeight={600} sx={{ fontSize: 36, textAlign: 'center' }}>
      {props.value}
    </Typography>
    <Typography fontWeight={600} sx={{ fontSize: 24, textAlign: 'center' }}>
      {props.label}
    </Typography>
  </div>
)

const CounterWidgetContent: React.FunctionComponent<CounterWidgetProps> = (props) => (
  <React.Fragment>
    {props.counters.length === 1 ? (
      <CounterItem {...props.counters[0]} />
    ) : (
      <Grid container spacing={1} direction="row" alignItems="center">
        {props.counters.map((counter, idx) => (
          <Grid item xs key={idx} component={Box} height={'100%'}>
            <Box>
              <CounterItem {...counter} />
            </Box>
          </Grid>
        ))}
      </Grid>
    )}
  </React.Fragment>
)

export default CounterWidgetContent
