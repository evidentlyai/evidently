import { EvidentlyLogoSvg } from 'evidently-ui-lib/components/LogoSvg'
import { NavigationProgress } from 'evidently-ui-lib/components/NavigationProgress'
import { ServiceHeader } from 'evidently-ui-lib/components/ServiceHeader'
import { BreadCrumbs } from 'evidently-ui-lib/router-utils/components/breadcrumbs'
import { getVersion } from 'evidently-ui-lib/routes-components/home/data'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet, ScrollRestoration } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import type { GetRouteByPath } from '~/_routes/types'

import { useCrumbsFromHandle, useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type CurrentRoute = GetRouteByPath<'/'>

const crumb: CrumbDefinition = { title: 'Home' }

export const handle = { crumb }

export const loader = () => getVersion({ api: clientAPI })

export const Component = () => {
  const { loaderData } = useRouteParams<CurrentRoute>()
  const { crumbs } = useCrumbsFromHandle()

  return (
    <>
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceHeader version={loaderData.version} LogoSvg={EvidentlyLogoSvg} />
      <Box p={3}>
        <BreadCrumbs crumbs={crumbs} />
        <Outlet />
      </Box>
    </>
  )
}
