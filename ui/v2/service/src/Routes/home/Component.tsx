import {
  Outlet,
  ScrollRestoration,
  ShouldRevalidateFunction,
  useLoaderData
} from 'react-router-dom'
// import { ThemeProvider } from '@mui/material/styles'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import 'dayjs/locale/en-gb'

import { api } from 'api/RemoteApi'

import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from 'Components'

import { isOnlySearchParamsChanges } from 'Utils/isOnlySearchParamsChanges'

export const loader = () => api.getVersion()
type loaderData = Awaited<ReturnType<typeof loader>>

export const shouldRevalidate: ShouldRevalidateFunction = (args) => {
  if (isOnlySearchParamsChanges(args)) {
    return false
  }

  return true
}

export const Component = () => {
  const { version } = useLoaderData() as loaderData

  return (
    // <ThemeProvider theme={theme}>
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <ServiceHeader version={version} />
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceMainPage>
        <Outlet />
      </ServiceMainPage>
    </LocalizationProvider>
    // </ThemeProvider>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
