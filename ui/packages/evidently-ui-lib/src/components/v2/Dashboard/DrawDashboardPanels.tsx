import type { DashboardPanelPlotModel } from 'evidently-ui-lib/api/types/v2'
import { Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'

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
      {panels.map((panel) => (
        <Grid item key={panel.id} {...getSizeForGridItem(panel.size)}>
          <PanelComponent panel={panel} />
        </Grid>
      ))}
    </Grid>
  )
}

const getSizeForGridItem = (
  size?: string | null
): {
  xs: 1 | 3 | 6 | 12
  sm: 1 | 3 | 6 | 12
  md: 1 | 3 | 6 | 12
  lg: 1 | 3 | 6 | 12
} => {
  if (size === 'full') {
    return { xs: 12, sm: 12, md: 12, lg: 12 }
  }
  if (size === 'half') {
    return { xs: 12, sm: 12, md: 6, lg: 6 }
  }

  return { xs: 12, sm: 12, md: 12, lg: 12 }
}
