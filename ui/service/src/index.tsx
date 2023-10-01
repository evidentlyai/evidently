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
import {
  ProjectList,
  action as projectListAction,
  loader as projectListLoader
} from './Components/ProjectList'
import { ServiceHeader } from './Components/ServiceHeader'
import { Box, FormControlLabel, Switch, Typography } from '@material-ui/core'
import { NavigationProgress } from './Components/NavigationProgress'
import { Project, PROJECT_TABS } from './Components/Projects2/Project'
import { Dashboard, loader as dashboardLoader } from './Components/Projects2/Dashboard'
import { ReportsList, loader as reportListLoader } from './Components/Projects2/Reports'
import { Report, loader as reportLoader } from './Components/Projects2/Report'
import { TestSuite, loader as testSuiteLoader } from './Components/Projects2/TestSuite'
import { TestSuitesList, loader as testSuitesListLoader } from './Components/Projects2/TestSuites'
import { useEffect, useState } from 'react'

const api = new RemoteApi('/api')

const HomePage = () => {
  let { projectId, dashboardId } = useParams()
  const [isNewVersion, setNewVersion] = useState(true)
  const navigate = useNavigate()
  const location = useLocation()

  // delete this code and switch after PR approve
  useEffect(() => {
    const url = `${location.pathname}${location.search}${location.hash}`

    const replaceArgs: [string, string][] = [
      ['projects', 'projects2'],
      ['test_suites', 'test-suites']
    ]

    if (isNewVersion) {
      navigate(replaceArgs.reduce((url, replacer) => url.replace(...replacer), url))
      return
    }
    navigate(
      replaceArgs.reduce(
        (url, replacer) => url.replace(...(replacer.reverse() as [string, string])),
        url
      )
    )
  }, [isNewVersion])

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
    path: '',
    element: <HomePage />,
    children: [
      {
        index: true,
        element: <ProjectList />,
        loader: projectListLoader,
        action: projectListAction,
        errorElement: <Typography variant="h4"> Something went wrong...</Typography>
      },
      {
        // Old version
        path: 'projects/:projectId/:page?/:reportId?',
        element: <ProjectData />
      },
      {
        // New version
        path: 'projects2/:projectId',
        element: <Project />,
        children: [
          {
            index: true,
            id: PROJECT_TABS[0].id,
            element: <Dashboard />,
            loader: dashboardLoader
          },
          {
            id: PROJECT_TABS[1].id,
            path: PROJECT_TABS[1].link,
            element: <ReportsList />,
            loader: reportListLoader,
            children: [
              {
                id: 'show-report-by-id',
                path: ':reportId',
                element: <Report />,
                loader: reportLoader
              }
            ]
          },
          {
            id: PROJECT_TABS[2].id,
            path: PROJECT_TABS[2].link,
            element: <TestSuitesList />,
            loader: testSuitesListLoader,
            children: [
              {
                id: 'show-test-suite-by-id',
                path: ':testSuiteId',
                element: <TestSuite />,
                loader: testSuiteLoader
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
