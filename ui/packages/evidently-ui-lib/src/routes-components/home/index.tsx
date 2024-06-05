import { Outlet, ScrollRestoration, useLoaderData } from 'react-router-dom'
import { NavigationProgress, BreadCrumbs, ServiceHeader, crumbFunction } from '~/components'
import type { LoaderData } from './data'
import { Box } from '@mui/material'
import { ActionErrorSnackbar } from '~/components/Error'

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
      <ActionErrorSnackbar />
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
