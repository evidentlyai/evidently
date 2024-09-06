import React from 'react'
import ReactDOM from 'react-dom/client'

import type { AdditionalGraphInfo } from 'evidently-ui-lib/api'
import { ThemeProvider } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { theme } from 'evidently-ui-lib/theme/v2'

import type { DashboardInfoModel } from 'evidently-ui-lib/api/types'
import { StandaloneSnapshotWidgets } from 'evidently-ui-lib/standalone/app'

export function drawDashboard(
  dashboard: DashboardInfoModel,
  additionalGraphs: Map<string, AdditionalGraphInfo>,
  tagId: string
) {
  const element = document.getElementById(tagId)
  if (element) {
    ReactDOM.createRoot(element).render(
      <React.StrictMode>
        <ThemeProvider theme={theme}>
          <StandaloneSnapshotWidgets dashboard={dashboard} additionalGraphs={additionalGraphs} />
        </ThemeProvider>
      </React.StrictMode>
    )
  }
}

// @ts-ignore
window.drawDashboard = drawDashboard
