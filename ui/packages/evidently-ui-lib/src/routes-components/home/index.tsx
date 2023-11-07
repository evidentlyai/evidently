import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from '~/components'
import 'dayjs/locale/en-gb'

import type { loaderData } from './data'

export const HomeComponentTemplate = ({ logoSrc }: { logoSrc: string }) => {
  const { version } = useLoaderData() as loaderData

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <ServiceHeader version={version} logoSrc={logoSrc} />
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceMainPage>
        <Outlet />
      </ServiceMainPage>
    </LocalizationProvider>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
