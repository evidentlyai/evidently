import React from 'react'
import ReactDOM from 'react-dom/client'

import { AdditionalGraphInfo, DashboardInfo } from 'evidently-ui/api'
import ApiContext from 'evidently-ui/contexts/ApiContext'
import LocalApi from 'evidently-ui/api/LocalApi'
import { theme } from 'evidently-ui/theme/v1'
import { ProjectReport } from 'evidently-ui/standalone/app'

import { ThemeProvider } from '@mui/material/styles'

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
