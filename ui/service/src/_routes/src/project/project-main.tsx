import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { ensureID } from 'evidently-ui-lib/api/utils'
import type { ActionSpecialArgs, GetParams } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { LoaderFunctionArgs } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { useRouteParams } from '~/_routes/hooks'
import type { GetRouteByPath } from '~/_routes/types'

import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

type Path = '/:projectId'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { param: 'projectId' satisfies keyof Params }

export const handle = { crumb }

export const actionSpecial = async (_args: ActionSpecialArgs<{ data: 123 }>) => {
  return null
}

export const loader = ({ params }: LoaderFunctionArgs) => {
  const { projectId } = params as Params

  return clientAPI
    .GET('/api/projects/{project_id}/info', { params: { path: { project_id: projectId } } })
    .then(responseParser())
    .then(ensureID)
}

export const Component = () => {
  const { loaderData } = useRouteParams<CurrentRoute>()

  console.log('loaderData', loaderData)

  return (
    <>
      <Typography align='center' variant='h5'>
        Project
      </Typography>
    </>
  )
}
