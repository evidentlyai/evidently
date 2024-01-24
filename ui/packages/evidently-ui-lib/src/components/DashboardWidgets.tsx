import { Grid } from '@mui/material'
import { WidgetInfo } from '~/api'
import { DashboardContentWidgets } from '~/components/DashboardContent'

export const DashboardWidgets = ({
  widgets,
  ItemWrapper
}: {
  widgets: WidgetInfo[]
  ItemWrapper?: ({ id, children }: { id: string; children: React.ReactNode }) => React.ReactNode
}) => {
  return (
    <>
      <Grid container spacing={3} direction="row" alignItems="stretch">
        <DashboardContentWidgets widgets={widgets} ItemWrapper={ItemWrapper} />
      </Grid>
    </>
  )
}
