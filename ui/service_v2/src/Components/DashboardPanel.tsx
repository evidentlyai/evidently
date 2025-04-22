import type { BatchMetricDataModel, DashboardPanelPlotModel } from 'evidently-ui-lib/api/types/v2'
import {
  DashboardPanel,
  type DashboardPanelProps
} from 'evidently-ui-lib/components/v2/Dashboard/DashboardPanel'
import type { PanelComponentType } from 'evidently-ui-lib/components/v2/Dashboard/DrawDashboardPanels'
import { PlotDashboardPanelSkeleton } from 'evidently-ui-lib/components/v2/Dashboard/Panels/DashboardPanel'
import { getSeriesListTypeHash } from 'evidently-ui-lib/components/v2/Dashboard/utils'
import { useParams } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useEffect } from 'react'
import invariant from 'tiny-invariant'
import { useLoader } from '~/routes/hooks'

const RenderPanelByDataFetch = ({ panel }: { panel: DashboardPanelPlotModel }) => {
  const { projectId } = useParams()
  invariant(projectId)

  const panelPointsFetcher = useLoader('/projects/:projectId/load-panel-points')
  const pointsData = panelPointsFetcher.data

  const seriesList = panel.values

  const seriesHashForTrackingChanges = getSeriesListTypeHash(seriesList)

  const originalPlotType = panel.plot_params?.plot_type

  const plotType: DashboardPanelProps['plotType'] =
    (originalPlotType === 'line' ||
    originalPlotType === 'bar' ||
    originalPlotType === 'text' ||
    originalPlotType === 'counter'
      ? originalPlotType
      : null) ?? 'line'

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (plotType === 'text') {
      return
    }

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

  // if (plotType !== 'text' && !pointsData ) {
  //   return <DashboardPanelSkeleton title={title} subtitle={subtitle} height={height} />
  // }

  if (plotType === 'bar' || plotType === 'line') {
    if (!pointsData) {
      return <PlotDashboardPanelSkeleton title={title} subtitle={subtitle} height={height} />
    }

    const isStacked = Boolean(panel.plot_params?.is_stacked)

    const legendMarginRight =
      typeof panel.plot_params?.legend_margin_right === 'number'
        ? Number(panel.plot_params?.legend_margin_right)
        : 300

    return (
      <DashboardPanel
        plotType={plotType}
        data={pointsData}
        height={height}
        legendMarginRight={legendMarginRight}
        isStacked={isStacked}
      />
    )
  }

  return <></>

  //   ////////////////////////////////////////////
  //   //  CAST `Panel` PARAMETERS
  //   ////////////////////////////////////////////

  //   const originalPlotType = panel.plot_params?.plot_type
  //   if (originalPlotType === 'text' || originalPlotType === 'counter') {
  //     return (
  //       <CustomDashboardPanel
  //         height={height}
  //         title={title}
  //         description={subtitle}
  //         data={pointsData}
  //         plotType={originalPlotType}
  //         counterAgg={panel.plot_params?.aggregation as string}
  //       />
  //     )
  //   }

  //   const plotType =
  //     (originalPlotType === 'line' || originalPlotType === 'bar' ? originalPlotType : null) ?? 'line'

  //   const isStacked = Boolean(panel.plot_params?.is_stacked)

  //   const legendMarginRight = panel.plot_params?.legend_margin_right
  //     ? Number(panel.plot_params?.legend_margin_right)
  //     : 300

  //   return (
  //     <DashboardPanel
  //       height={height}
  //       title={title}
  //       description={subtitle}
  //       data={pointsData}
  //       plotType={plotType}
  //       isStacked={isStacked}
  //       legendMarginRight={legendMarginRight}
  //     />
  //   )
}

export const PanelComponet: PanelComponentType = RenderPanelByDataFetch
