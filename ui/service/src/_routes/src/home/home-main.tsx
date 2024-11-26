import { BreadCrumbs2 } from 'evidently-ui-lib/components/BreadCrumbs'
import { EvidentlyLogoSvg } from 'evidently-ui-lib/components/LogoSvg'
import { NavigationProgress } from 'evidently-ui-lib/components/NavigationProgress'
import { ServiceHeader } from 'evidently-ui-lib/components/ServiceHeader'
import { getVersion } from 'evidently-ui-lib/routes-components/home/data'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import {
  type LoaderFunctionArgs,
  Outlet,
  ScrollRestoration
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { useRouteParams } from '~/_routes/hooks'
import type { GetRouteByPath } from '~/_routes/types'

import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { clientAPI } from '~/api'
import { useCrumbs } from './hooks'

///////////////////
//    ROUTE
///////////////////

type CurrentRoute = GetRouteByPath<'/'>

const crumb: CrumbDefinition = { title: 'Home' }

export const handle = { crumb }

export const loader = (_args: LoaderFunctionArgs) => getVersion({ api: clientAPI })

export const Component = () => {
  const { loaderData } = useRouteParams<CurrentRoute>()
  const { crumbs } = useCrumbs()

  return (
    <>
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceHeader version={loaderData.version} LogoSvg={EvidentlyLogoSvg} />
      <Box p={3}>
        <BreadCrumbs2 crumbs={crumbs} />
        <Outlet />
      </Box>
    </>
  )
}
