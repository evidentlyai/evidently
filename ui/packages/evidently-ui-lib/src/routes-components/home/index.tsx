import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { NavigationProgress, BreadCrumbs, ServiceHeader, crumbFunction } from '~/components'
import type { loaderData } from './data'
import { Box } from '@mui/material'

export const HomeComponentTemplate = ({
  logoSrc,
  authComponent
}: {
  logoSrc: string
  authComponent?: React.ReactNode
}) => {
  const { version } = useLoaderData() as loaderData

  return (
    <>
      <ServiceHeader authComponent={authComponent} version={version} logoSrc={logoSrc} />
      <NavigationProgress />
      <ScrollRestoration />
      <Box p={3}>
        <BreadCrumbs />
        <Outlet />
      </Box>
    </>
  )
}

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
