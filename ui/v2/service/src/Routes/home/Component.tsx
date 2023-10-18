import { Outlet, useLoaderData } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import 'dayjs/locale/en-gb'

import { api } from 'api/RemoteApi'

import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from 'Components'
import { theme } from 'evidently-ui/theme'

export const loader = () => api.getVersion()

type loaderData = Awaited<ReturnType<typeof loader>>

export const Component = () => {
  const { version } = useLoaderData() as loaderData

  return (
    <ThemeProvider theme={theme}>
      <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
        <ServiceHeader version={version} />
        <NavigationProgress />
        <ServiceMainPage>
          <Outlet />
        </ServiceMainPage>
      </LocalizationProvider>
    </ThemeProvider>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
