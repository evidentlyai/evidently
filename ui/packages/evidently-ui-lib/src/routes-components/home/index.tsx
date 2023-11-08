import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { NavigationProgress, ServiceMainPage, ServiceHeader, crumbFunction } from '~/components'
import 'dayjs/locale/en-gb'

import type { loaderData } from './data'

export const HomeComponentTemplate = ({
  logoSrc,
  authComponent
}: {
  logoSrc: string
  authComponent?: React.ReactNode
}) => {
  const { version } = useLoaderData() as loaderData

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <ServiceHeader authComponent={authComponent} version={version} logoSrc={logoSrc} />
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
