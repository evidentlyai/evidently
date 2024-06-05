import { getDashboardProvider } from 'evidently-ui-lib/api/providers/dashboard'
import { getProjectsProvider } from 'evidently-ui-lib/api/providers/projects'
import { getVersionProvider } from 'evidently-ui-lib/api/providers/version'
import { createRemoteDashboardAPI } from 'evidently-ui-lib/api/RemoteDashboardAPI'

export const dashboardProvider = getDashboardProvider('/')
export const projectProvider = getProjectsProvider('/')
export const versionProvider = getVersionProvider('/')

export const remoteDashboardAPI = createRemoteDashboardAPI(dashboardProvider)
