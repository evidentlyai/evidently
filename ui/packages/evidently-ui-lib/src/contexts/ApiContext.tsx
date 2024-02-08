import React from 'react'

import {
  Api,
  AdditionalGraphInfo,
  DashboardInfo,
  ProjectDetails,
  ProjectInfo,
  SnapshotInfo,
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

  getReports(): Promise<SnapshotInfo[]> {
    return Promise.reject('not implemented')
  }

  getProjectInfo(): Promise<ProjectDetails> {
    return Promise.reject('not implemented')
  }

  getTestSuites(): Promise<SnapshotInfo[]> {
    return Promise.reject('not implemented')
  }

  getVersion(): Promise<VersionInfo> {
    return Promise.reject('not implemented')
  }

  createProject(_project: Partial<ProjectDetails>): Promise<ProjectDetails> {
    return Promise.reject('not implemented')
  }

  editProjectInfo(_project: ProjectDetails) {
    return Promise.reject('not implemented')
  }

  reloadProject(_projectId: string): Promise<Response> {
    return Promise.reject('not implemented')
  }

  deleteProject(_projectId: string): Promise<Response> {
    return Promise.reject('not implemented')
  }
}

const ApiContext = React.createContext<ApiContextState>({ Api: new NotImplementedApi() })

export default ApiContext
