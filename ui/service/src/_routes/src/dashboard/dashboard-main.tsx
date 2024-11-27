import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'

import type { LoaderFunctionArgs } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

import { useRouteParams } from '~/_routes/hooks'
import type { GetRouteByPath } from '~/_routes/types'

import { getProjectDashboard } from 'evidently-ui-lib/routes-components/dashboard/data'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

export const index = true as const

type Path = '/:projectId/?index'

type CurrentRoute = GetRouteByPath<Path>

type Params = GetParams<Path>

const crumb: CrumbDefinition = { title: 'Dashboard' }

export const handle = { crumb }

export const loader = ({ params /* request */ }: LoaderFunctionArgs) => {
  const { projectId: project_id } = params as Params

  // const { searchParams } = new URL(request.url)

  return getProjectDashboard({
    api: clientAPI,
    project_id,
    timestamp_start: null,
    timestamp_end: null
  })
}

export const Component = () => {
  const { loaderData: data } = useRouteParams<CurrentRoute>()

  console.log(data)

  // return <ProjectDashboard data={data} />

  return (
    <p>
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Delectus provident voluptatibus
      accusamus molestiae illo, ullam aut nihil error numquam nesciunt cum tenetur rem quis
      voluptatem voluptate ratione? Qui, doloremque mollitia.
    </p>
  )
}
