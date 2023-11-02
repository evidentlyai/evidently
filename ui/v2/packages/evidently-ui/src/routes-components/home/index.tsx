import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from '~/components'
import 'dayjs/locale/en-gb'
import { Theme } from '@mui/material/styles'

import type { loaderData } from './data'

export const HomeComponentTemplate = ({ theme, logoSrc }: { theme: Theme; logoSrc: string }) => {
  const { version } = useLoaderData() as loaderData

  return (
    <ThemeProvider theme={theme}>
      <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
        <ServiceHeader version={version} logoSrc={logoSrc} />
        <NavigationProgress />
        <ScrollRestoration />
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
