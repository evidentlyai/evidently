import React from 'react'
import ReactDOM from 'react-dom/client'

import { AdditionalGraphInfo, DashboardInfo } from 'evidently-ui-lib/api'
import ApiContext from 'evidently-ui-lib/contexts/ApiContext'
import LocalApi from 'evidently-ui-lib/api/LocalApi'
import { ThemeProvider } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { theme } from 'evidently-ui-lib/theme/v2'

import { ProjectReport } from 'evidently-ui-lib/standalone/app'

export function drawDashboard(
  dashboard: DashboardInfo,
  additionalGraphs: Map<string, AdditionalGraphInfo>,
  tagId: string
) {
  ReactDOM.createRoot(document.getElementById(tagId)!).render(
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <ApiContext.Provider value={{ Api: new LocalApi(dashboard, additionalGraphs) }}>
          <ProjectReport projectId={'p1'} reportId={'d1'} />
        </ApiContext.Provider>
      </ThemeProvider>
    </React.StrictMode>
  )
}

// @ts-ignore
window.drawDashboard = drawDashboard
