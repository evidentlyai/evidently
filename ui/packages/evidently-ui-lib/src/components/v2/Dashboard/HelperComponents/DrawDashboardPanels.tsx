import type { DashboardPanelPlotModel } from 'evidently-ui-lib/api/types/v2'
import { Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  castRawPanelDataToDashboardPanelProps,
  getSizeForGridItem
} from '~/components/v2/Dashboard/utils'

export type PanelComponentType = (args: { panel: DashboardPanelPlotModel }) => JSX.Element

export const DrawDashboardPanels = ({
  panels,
  PanelComponent
}: { panels: DashboardPanelPlotModel[]; PanelComponent: PanelComponentType }) => {
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
            <PanelComponent panel={panel} />
          </Grid>
        )
      })}
    </Grid>
  )
}
