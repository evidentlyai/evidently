import ReactDOM from 'react-dom'
import './index.css'

import { createTheme, ThemeProvider } from '@material-ui/core/styles'
import reportWebVitals from './reportWebVitals'
import RemoteApi from './api/RemoteApi'
import ApiContext from './lib/contexts/ApiContext'
import {
  createBrowserRouter,
  Outlet,
  RouterProvider,
  useLocation,
  useNavigate,
  useParams
} from 'react-router-dom'
import './index.css'
import { ServiceMainPage, ServiceMainPageOld } from './Components/ServiceMainPage'
import { ProjectData } from './Components/ProjectData'
import ProjectListRoute from './Components/ProjectList'
import { ServiceHeader } from './Components/ServiceHeader'
import { Box, FormControlLabel, Switch } from '@material-ui/core'
import { NavigationProgress } from './Components/NavigationProgress'
import ProjectRoute from './Components/Projects2/Project'
import DashboardRoute from './Components/Projects2/Dashboard'
import ReportsRoute from './Components/Projects2/Reports'
import ReportRoute from './Components/Projects2/Report'
import TestSuiteRoute from './Components/Projects2/TestSuite'
import TestSuitesRoute from './Components/Projects2/TestSuites'
import { useEffect, useState } from 'react'

const api = new RemoteApi('/api')

const HomePage = () => {
  let { projectId, dashboardId } = useParams()
  const [isNewVersion, setNewVersion] = useState(true)
  const navigate = useNavigate()
  const location = useLocation()

  // Delete this code and switch after PR approve
  useEffect(() => {
    const url = `${location.pathname}${location.search}${location.hash}`

    const replaceUrlArgs: [string, string][] = [
      ['/projects/', '/projects2/'],
      ['/test_suites', '/test-suites']
    ]

    if (isNewVersion) {
      navigate(replaceUrlArgs.reduce((url, replacer) => url.replace(...replacer), url))
      return
    }

    navigate(
      replaceUrlArgs.reduce(
        (url, replacer) => url.replace(...(replacer.reverse() as [string, string])),
        url
      )
    )
  }, [isNewVersion])

  // Delete this code and switch after PR approve
  const SMPComponent = isNewVersion ? ServiceMainPage : ServiceMainPageOld

  return (
    <ThemeProvider theme={theme}>
      <ApiContext.Provider value={{ Api: api }}>
        <ServiceHeader api={api} />
        <NavigationProgress />
        <Box ml={3} my={2}>
          <FormControlLabel
            control={
              <Switch
                onChange={() => setNewVersion((prev) => !prev)}
                checked={isNewVersion}
                color="primary"
              />
            }
            label="Use new version"
            labelPlacement="end"
          />
        </Box>
        <SMPComponent projectId={projectId} reportId={dashboardId}>
          <Outlet context={{ isNewVersion }} />
        </SMPComponent>
      </ApiContext.Provider>
    </ThemeProvider>
  )
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
    handle: {
      crumb: () => ({ to: '/', linkText: 'Home' })
    },
    children: [
      { ...ProjectListRoute, index: true },
      {
        // Old version (for better manual testing)
        path: 'projects/:projectId/:page?/:reportId?',
        element: <ProjectData />
      },
      {
        // New version
        ...ProjectRoute,
        children: [
          {
            ...DashboardRoute,
            index: true
          },
          {
            ...ReportsRoute,
            children: [
              {
                ...ReportRoute
              }
            ]
          },
          {
            ...TestSuitesRoute,
            children: [
              {
                ...TestSuiteRoute
              }
            ]
          }
        ]
      }
    ]
  }
])

export const theme = createTheme({
  shape: {
    borderRadius: 0
  },
  palette: {
    primary: {
      light: '#ed5455',
      main: '#ed0400',
      dark: '#d40400',
      contrastText: '#fff'
    },
    secondary: {
      light: '#61a0ff',
      main: '#3c7fdd',
      dark: '#61a0ff',
      contrastText: '#000'
    }
  },
  typography: {
    button: {
      fontWeight: 'bold'
    },
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"'
    ].join(',')
  }
})

ReactDOM.render(
  <>
    <RouterProvider router={router} />
  </>,
  document.getElementById('root') as HTMLElement
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
