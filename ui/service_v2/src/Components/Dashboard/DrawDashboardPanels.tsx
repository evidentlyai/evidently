import type { BatchMetricDataModel, DashboardModel } from 'api/types'
import { useWidgetWrapper } from 'evidently-ui-lib/contexts/WidgetWrapper'
import { Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useEffect } from 'react'
import type React from 'react'
import { useLoader } from 'routes/hooks'
import { DashboardPanel } from './DashboardPanel'
import { DashboardPanelSkeleton } from './DashboardPanelSkeleton'
import { getSeriesListTypeHash } from './utils'

type Panels = DashboardModel['panels']
type PanelType = Panels[number]

export const DrawDashboardPanels = ({ panels }: { panels: Panels }) => {
  if (panels.length === 0) {
    return (
      <Typography my={3} align='center' variant='h4'>
        This dashboard is currently empty. Please add a monitoring panel to start.
      </Typography>
    )
  }

  return <DrawPanels panels={panels} />
}

const DrawPanels: React.FC<{ panels: Panels }> = ({ panels }) => (
  <Grid container spacing={3} direction='row' alignItems='stretch'>
    {panels.map((panel) => (
      <Grid item key={panel.id} {...getSizeForGridItem(panel.size)}>
        <PanelWrapper id={panel.id ?? ''}>
          <RenderPanelByDataFetch panel={panel} />
        </PanelWrapper>
      </Grid>
    ))}
  </Grid>
)

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

const RenderPanelByDataFetch = ({ panel }: { panel: PanelType }) => {
  const { projectId } = useParams()
  const panelPointsFetcher = useLoader('/v2/projects/:projectId/api/load-panel-points')
  const pointsData = panelPointsFetcher.data

  const seriesList = panel.values

  const seriesHashForTrackingChanges = getSeriesListTypeHash(seriesList)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    panelPointsFetcher.load({
      paramsToReplace: { projectId },
      query: {
        body: JSON.stringify({
          series_filter: seriesList.map((s) => ({
            metric: s.metric,
            tags: s.tags ?? [],
            metadata: s.metadata ?? {},
            metric_labels: s.metric_labels ?? {}
          }))
        } satisfies BatchMetricDataModel)
      }
    })
  }, [seriesHashForTrackingChanges])

  const height = 350

  const title = panel.title ?? ''
  const subtitle = panel.subtitle ?? ''

  if (!pointsData) {
    return <DashboardPanelSkeleton title={title} subtitle={subtitle} height={height} />
  }

  ////////////////////////////////////////////
  //  CAST `Panel` PARAMETERS
  ////////////////////////////////////////////

  const plotType =
    (panel.plot_params?.plot_type === 'line' || panel.plot_params?.plot_type === 'bar'
      ? panel.plot_params.plot_type
      : null) ?? 'line'

  const isStacked = Boolean(panel.plot_params?.is_stacked)

  const legendMarginRight = panel.plot_params?.legend_margin_right
    ? Number(panel.plot_params?.legend_margin_right)
    : 300

  return (
    <DashboardPanel
      height={height}
      title={title}
      description={subtitle}
      data={pointsData}
      plotType={plotType}
      isStacked={isStacked}
      legendMarginRight={legendMarginRight}
    />
  )
}

const PanelWrapper = ({ children, id }: { children: React.ReactNode; id: string }) => {
  const { WidgetWrapper } = useWidgetWrapper()

  return <WidgetWrapper id={id}>{children}</WidgetWrapper>
}
