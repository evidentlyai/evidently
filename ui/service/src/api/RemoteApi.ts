import { getDashboardProvider } from 'evidently-ui-lib/api/providers/dashboard'
import { getProjectsProvider } from 'evidently-ui-lib/api/providers/projects'
import { getVersionProvider } from 'evidently-ui-lib/api/providers/version'
import { RemoteApi } from 'evidently-ui-lib/api/RemoteApi'

// TODO: Remove it later
export const api = new RemoteApi('/api')

export const projectProvider = getProjectsProvider('/')
export const dashboardProvider = getDashboardProvider('/')
export const versionProvider = getVersionProvider('/')
