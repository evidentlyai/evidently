import type React from 'react'

import { Box, Divider, Grid, Typography } from '@mui/material'

interface WidgetGroupProps {
  title: string
  children: React.ReactNode
}

const WidgetGroup: React.FunctionComponent<WidgetGroupProps> = (props) => (
  <Grid item xs={12} component={Box}>
    <Typography variant={'h5'}>{props.title}</Typography>
    <Grid container spacing={3} padding={10}>
      {props.children}
    </Grid>
    <Divider />
  </Grid>
)

export default WidgetGroup
