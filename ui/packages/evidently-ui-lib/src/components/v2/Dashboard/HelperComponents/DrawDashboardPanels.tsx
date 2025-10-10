import type {
  DashboardModel,
  DashboardPanelPlotModel,
  DashboardTabModel
} from 'evidently-ui-lib/api/types'
import { Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  castRawPanelDataToDashboardPanelProps,
  getSizeForGridItem
} from '~/components/v2/Dashboard/utils'

export type PanelComponentType = (args: {
  panel: DashboardPanelPlotModel
  tab?: DashboardTabModel
  dashboard: DashboardModel
}) => JSX.Element

export const DrawDashboardPanels = ({
  panels,
  tab,
  dashboard,
  PanelComponent
}: {
  panels: DashboardPanelPlotModel[]
  tab?: DashboardTabModel
  dashboard: DashboardModel
  PanelComponent: PanelComponentType
}) => {
  if (panels.length === 0) {
    return (
      <Typography my={3} align='center' variant='h4'>
        This dashboard is currently empty. Please add a monitoring panel to start.
      </Typography>
    )
  }

  return (
    <Grid container spacing={3} direction='row' alignItems='stretch'>
      {panels.map((panel) => {
        const dashboardPanelProps = castRawPanelDataToDashboardPanelProps(panel)

        return (
          <Grid key={panel.id} size={getSizeForGridItem(dashboardPanelProps.size)}>
            <PanelComponent panel={panel} tab={tab} dashboard={dashboard} />
          </Grid>
        )
      })}
    </Grid>
  )
}
