import { useEffect } from 'react'
import type { DashboardPanelPlotModel, SeriesModel } from '~/api/types'
import { DashboardPanel } from '~/components/v2/Dashboard/Panels/DashboardPanel'
import { DashboardPanelSkeleton } from '~/components/v2/Dashboard/Panels/Skeleton'
import { castRawPanelDataToDashboardPanelProps } from '../utils'

type RenderPanelByDataFetchGeneralComponentProps = {
  panel: DashboardPanelPlotModel
  loadDataPointsCallback: () => void
  loadDataPointsHash: string
  data?: SeriesModel
}

export const RenderPanelByDataFetchGeneralComponent = (
  props: RenderPanelByDataFetchGeneralComponentProps
) => {
  const { panel, loadDataPointsCallback, loadDataPointsHash, data } = props

  const dashboardPanelProps = castRawPanelDataToDashboardPanelProps(panel)

  const isNeedToFetchData = dashboardPanelProps.type !== 'text'

  const height = 'height' in dashboardPanelProps ? dashboardPanelProps.height : 200

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (!isNeedToFetchData) {
      return
    }

    loadDataPointsCallback()
  }, [loadDataPointsHash, isNeedToFetchData])

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
