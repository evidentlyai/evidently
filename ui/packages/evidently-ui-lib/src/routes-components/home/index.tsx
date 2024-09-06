import { Box } from '@mui/material'
import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { BreadCrumbs, NavigationProgress, ServiceHeader, type crumbFunction } from '~/components'
import type { LoaderData } from './data'

export const HomeComponentTemplate = ({
  logoSrc,
  authComponent
}: {
  logoSrc: string
  authComponent?: React.ReactNode
}) => {
  const { version } = useLoaderData() as LoaderData

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

export const handle: { crumb: crumbFunction<LoaderData> } = {
  crumb: () => ({ to: '/', linkText: 'Home' })
}
