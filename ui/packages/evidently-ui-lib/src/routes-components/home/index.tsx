import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import {
  NavigationProgress,
  ServiceMainPage,
  ServiceHeader,
  crumbFunction,
  BreadCrumbs
} from '~/components'
import 'dayjs/locale/en-gb'

import type { loaderData } from './data'
import { Box } from '@mui/material'
import { SideBarLink } from '~/components/Sidebar'

export const HomeComponentTemplate = ({
  logoSrc,
  authComponent,
  sideBarSettings = {}
}: {
  logoSrc: string
  authComponent?: React.ReactNode
  sideBarSettings?: {
    additionalProjectLinks?: SideBarLink[]
    globalLinks?: SideBarLink[]
  }
}) => {
  const { version } = useLoaderData() as loaderData

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <ServiceHeader authComponent={authComponent} version={version} logoSrc={logoSrc} />
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceMainPage sideBarSettings={sideBarSettings}>
        <Box p={3}>
          <BreadCrumbs />
          <Outlet />
        </Box>
      </ServiceMainPage>
    </LocalizationProvider>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
