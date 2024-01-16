import { Grid } from '@mui/material'
import { WidgetInfo } from '~/api'
import { DashboardContentWidgets } from '~/components/DashboardContent'

export const DashboardWidgets = ({ widgets }: { widgets: WidgetInfo[] }) => {
  return (
    <>
      <Grid container spacing={3} direction="row" alignItems="stretch">
        <DashboardContentWidgets widgets={widgets} />
      </Grid>
    </>
  )
}
