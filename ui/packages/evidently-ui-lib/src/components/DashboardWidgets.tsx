import { Typography } from '@mui/material'
import type { WidgetInfo } from '~/api'
import { DrawWidgets } from '~/components/WidgetsContent'

export const DashboardWidgets = ({ widgets }: { widgets: WidgetInfo[] }) => {
  if (widgets.length === 0) {
    return (
      <Typography my={3} align='center' variant='h4'>
        This dashboard is currently empty. Please add a monitoring panel to start.
      </Typography>
    )
  }

  return <DrawWidgets widgets={widgets} />
}
