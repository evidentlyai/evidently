import type { BatchMetricDataModel, DashboardPanelPlotModel } from 'evidently-ui-lib/api/types'
import type { PanelComponentType } from 'evidently-ui-lib/components/v2/Dashboard/HelperComponents/DrawDashboardPanels'
import { RenderPanelByDataFetchGeneralComponent } from 'evidently-ui-lib/components/v2/Dashboard/HelperComponents/RenderPanelByDataFetchGeneralComponent'
import { getPanelValuesTypeHash } from 'evidently-ui-lib/components/v2/Dashboard/utils'
import invariant from 'tiny-invariant'
import { useProjectInfo } from '~/contexts/project'
import { useLoader } from '~/routes/hooks'

type RenderPanelByDataFetchProps = {
  panel: DashboardPanelPlotModel
}

const RenderPanelByDataFetch = (props: RenderPanelByDataFetchProps) => {
  const { panel } = props

  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project

  const panelPointsFetcher = useLoader('/projects/:projectId/load-panel-points')

  const { data } = panelPointsFetcher

  const panelValues = panel.values

  const payload: BatchMetricDataModel = {
    series_filter: panelValues.map((value) => ({
      metric: value.metric,
      tags: value.tags ?? [],
      metadata: value.metadata ?? {},
      metric_labels: value.metric_labels ?? {}
    }))
  }

  const loadDataPointsHash = getPanelValuesTypeHash(panelValues)

  const loadDataPointsCallback = () => {
    panelPointsFetcher.load({
      query: { body: JSON.stringify(payload) },
      paramsToReplace: { projectId }
    })
  }

  return (
    <RenderPanelByDataFetchGeneralComponent
      panel={panel}
      loadDataPointsCallback={loadDataPointsCallback}
      loadDataPointsHash={loadDataPointsHash}
      data={data}
    />
  )
}

export const PanelComponent: PanelComponentType = RenderPanelByDataFetch
