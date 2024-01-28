import React from 'react'

import { Grid } from '@mui/material'

interface WidgetPanelProps {
  children: React.ReactNode
}

class WidgetPanel extends React.Component<WidgetPanelProps> {
  render() {
    return (
      <Grid container alignItems={'stretch'} spacing={1} direction={'row'} mt={1}>
        {this.props.children}
      </Grid>
    )
  }
}

export default WidgetPanel
