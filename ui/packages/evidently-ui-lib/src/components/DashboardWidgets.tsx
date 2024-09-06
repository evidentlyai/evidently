import { Grid, Typography } from '@mui/material'
import type { WidgetInfo } from '~/api'
import { DashboardContentWidgets } from '~/components/DashboardContent'

export const DashboardWidgets = ({
  widgets,
  ItemWrapper
}: {
  widgets: WidgetInfo[]
  ItemWrapper?: ({ id, children }: { id: string; children: React.ReactNode }) => React.ReactNode
}) => {
  if (widgets.length === 0) {
    return (
      <Typography my={3} align='center' variant='h4'>
        This dashboard is currently empty. Please add a monitoring panel to start.
      </Typography>
    )
  }

  return (
    <>
      <Grid container spacing={3} direction='row' alignItems='stretch'>
        <DashboardContentWidgets widgets={widgets} ItemWrapper={ItemWrapper} />
      </Grid>
    </>
  )
}
