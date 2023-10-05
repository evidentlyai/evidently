import { Outlet } from 'react-router-dom'
import { ThemeProvider } from '@material-ui/core'

import ApiContext from 'lib/contexts/ApiContext'
import { api } from 'api/RemoteApi'
import { NavigationProgress } from 'Components/NavigationProgress'
import { ServiceMainPage } from 'Components/ServiceMainPage'
import { ServiceHeader } from 'Components/ServiceHeader'
import { crumbFunction } from 'Components/BreadCrumbs'
import { theme } from './theme'

export const Component = () => {
  return (
    <ThemeProvider theme={theme}>
      <ApiContext.Provider value={{ Api: api }}>
        <ServiceHeader api={api} />
        <NavigationProgress />
        <ServiceMainPage>
          <Outlet />
        </ServiceMainPage>
      </ApiContext.Provider>
    </ThemeProvider>
  )
}
export const handle: { crumb: crumbFunction<any> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
