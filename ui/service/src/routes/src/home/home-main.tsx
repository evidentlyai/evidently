import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ServiceHeader } from 'evidently-ui-lib/components/ServiceHeader'
import { BreadCrumbs } from 'evidently-ui-lib/router-utils/components/breadcrumbs'
import {
  FetchersProgress,
  NavigationProgress
} from 'evidently-ui-lib/router-utils/components/navigation-progress'
import { useCrumbsFromHandle, useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import { Box, Stack } from 'evidently-ui-lib/shared-dependencies/mui-material'
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
        <Stack direction={'row'} alignItems={'center'} gap={2}>
          <BreadCrumbs crumbs={crumbs} />
          <FetchersProgress />
        </Stack>
        <Outlet />
      </Box>
    </>
  )
}
