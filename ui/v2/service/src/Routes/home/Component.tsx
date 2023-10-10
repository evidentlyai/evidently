import { Outlet, useLoaderData } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'

import { api } from 'api/RemoteApi'

import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from 'Components'
import { theme } from './theme'

export const loader = () => api.getVersion()

type loaderData = Awaited<ReturnType<typeof loader>>

export const Component = () => {
  const { version } = useLoaderData() as loaderData

  return (
    <ThemeProvider theme={theme}>
      <ServiceHeader version={version} />
      <NavigationProgress />
      <ServiceMainPage>
        <Outlet />
      </ServiceMainPage>
    </ThemeProvider>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
