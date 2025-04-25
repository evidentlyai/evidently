import { useEffect } from 'react'
import type { DashboardPanelPlotModel, SeriesModel } from '~/api/types/v2'
import { DashboardPanel } from '~/components/v2/Dashboard/Panels/DashboardPanel'
import { DashboardPanelSkeleton } from '~/components/v2/Dashboard/Panels/Skeleton'
import { castRawPanelDataToDashboardPanelProps, getSeriesListTypeHash } from '../utils'

type RenderPanelByDataFetchGeneralComponentProps = {
  panel: DashboardPanelPlotModel
  loadDataForPanel: () => void
  data?: SeriesModel
}

export const RenderPanelByDataFetchGeneralComponent = ({
  panel,
  loadDataForPanel,
  data
}: RenderPanelByDataFetchGeneralComponentProps) => {
  const dashboardPanelProps = castRawPanelDataToDashboardPanelProps(panel)

  const isNeedToFetchData = dashboardPanelProps.type !== 'text'

  const seriesHashForTrackingChanges = getSeriesListTypeHash(panel.values)

  const height = 'height' in dashboardPanelProps ? dashboardPanelProps.height : 200

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (!isNeedToFetchData) {
      return
    }

    loadDataForPanel()
  }, [seriesHashForTrackingChanges, isNeedToFetchData])

  if (!isNeedToFetchData) {
    return <DashboardPanel {...dashboardPanelProps} />
  }

  if (!data) {
    return (
      <DashboardPanelSkeleton
        title={dashboardPanelProps.title}
        subtitle={dashboardPanelProps.description}
        height={height}
      />
    )
  }

  return <DashboardPanel {...dashboardPanelProps} data={data} />
}
