import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { NavigationProgress } from 'evidently-ui-lib/components/NavigationProgress'
import { ServiceHeader } from 'evidently-ui-lib/components/ServiceHeader'
import { BreadCrumbs } from 'evidently-ui-lib/router-utils/components/breadcrumbs'
import { useCrumbsFromHandle, useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import { Box } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { Outlet, ScrollRestoration } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'
import { HomeLink } from './components'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Home' }

export const handle = { crumb }

export const loadData = () => clientAPI.GET('/api/version').then(responseParser())

export const Component = () => {
  const { loaderData } = useCurrentRouteParams<CurrentRoute>()
  const { crumbs } = useCrumbsFromHandle()

  return (
    <>
      <NavigationProgress />
      <ScrollRestoration />
      <ServiceHeader version={loaderData.version} HomeLink={HomeLink} />
      <Box p={3}>
        <BreadCrumbs crumbs={crumbs} />
        <Outlet />
      </Box>
    </>
  )
}
