import type { BatchMetricDataModel } from 'evidently-ui-lib/api/types'
import type { PanelComponentType } from 'evidently-ui-lib/components/Dashboard/GeneralHelpers/DrawDashboardPanels'
import { RenderPanelByDataFetchGeneralComponent } from 'evidently-ui-lib/components/Dashboard/GeneralHelpers/RenderPanelByDataFetchGeneralComponent'
import {
  castRawPanelDataToDashboardPanelProps,
  getPanelValuesTypeHash
} from 'evidently-ui-lib/components/Dashboard/utils'
import { OneTimeHint } from 'evidently-ui-lib/components/Plots/OneTimeHint'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { useState } from 'react'
import invariant from 'tiny-invariant'
import { useProjectInfo } from '~/contexts/project'
import { useLoader } from '~/routes/type-safe-route-helpers/hooks'

const RenderPanelByDataFetch: PanelComponentType = (props) => {
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

const RenderPanelByDataFetchWithHint: PanelComponentType = (props) => {
  const { panel } = props
  const [isHovered, setIsHovered] = useState(false)

  const panelParsed = castRawPanelDataToDashboardPanelProps(panel)

  return (
    <>
      {isHovered && (
        <OneTimeHint
          storageKey='click-on-datapoints-one-time-hint'
          hintMessage='You can click on the data point to open the Report.'
        />
      )}

      <Box
        onMouseEnter={() => {
          if (panelParsed.type === 'line' || panelParsed.type === 'bar') {
            if (isHovered) {
              return
            }

            setIsHovered(true)
          }
        }}
      >
        <RenderPanelByDataFetch panel={panel} />
      </Box>
    </>
  )
}

export const PanelComponent: PanelComponentType = RenderPanelByDataFetchWithHint
