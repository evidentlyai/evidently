import React from 'react'

import {
  Api,
  AdditionalGraphInfo,
  DashboardInfo,
  ProjectDetails,
  ProjectInfo,
  ReportInfo,
  TestSuiteInfo,
  WidgetInfo,
  VersionInfo
} from '~/api'

interface ApiContextState {
  Api: Api
}

class NotImplementedApi implements Api {
  getAdditionalGraphData(): Promise<AdditionalGraphInfo> {
    return Promise.reject('not implemented')
  }

  getAdditionalWidgetData(): Promise<WidgetInfo> {
    return Promise.reject('not implemented')
  }

  getDashboard(): Promise<DashboardInfo> {
    return Promise.reject('not implemented')
  }

  getProjects(): Promise<ProjectInfo[]> {
    return Promise.reject('not implemented')
  }

  getProjectDashboard(): Promise<DashboardInfo> {
    return Promise.reject('not implemented')
  }

  getReports(): Promise<ReportInfo[]> {
    return Promise.reject('not implemented')
  }

  getProjectInfo(): Promise<ProjectDetails> {
    return Promise.reject('not implemented')
  }

  getTestSuites(): Promise<TestSuiteInfo[]> {
    return Promise.resolve([])
  }

  getVersion(): Promise<VersionInfo> {
    return Promise.resolve({ version: '0.0.0' })
  }

  editProjectInfo(_project: ProjectDetails) {
    return Promise.resolve()
  }
}

const ApiContext = React.createContext<ApiContextState>({ Api: new NotImplementedApi() })

export default ApiContext
