import type { DashboardPanelPlotModel } from 'evidently-ui-lib/api/types'
import { Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  castRawPanelDataToDashboardPanelProps,
  getSizeForGridItem
} from '~/components/v2/Dashboard/utils'

type PanelComponentProps = { panel: DashboardPanelPlotModel }
export type PanelComponentType = (props: PanelComponentProps) => JSX.Element

type DrawDashboardPanelsProps = {
  panels: DashboardPanelPlotModel[]
  PanelComponent: PanelComponentType
}

export const DrawDashboardPanels = (props: DrawDashboardPanelsProps) => {
  const { panels, PanelComponent } = props

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
