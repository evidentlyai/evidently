import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import {
  getProjects,
  getProjectsListActionSpecial
} from 'evidently-ui-lib/routes-components/projectsList/data'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { AddNewProjectWrapper, ProjectCardWrapper } from './components'

///////////////////
//    ROUTE
///////////////////

export const _route_path = '/?index'
type Path = typeof _route_path

export type CurrentRoute = GetRouteByPath<Path>

const crumb: CrumbDefinition = { title: 'Projects' }
export const handle = { crumb }

export const loaderSpecial = () => getProjects({ api: clientAPI })

export const actionSpecial = getProjectsListActionSpecial({ api: clientAPI })

export const Component = () => {
  const { loaderData: projects } = useRouteParams<CurrentRoute>()

  return (
    <>
      <Typography align='center' variant={'h5'}>
        {projects.length > 0 ? 'Project List' : "You don't have any projects yet"}
      </Typography>
      <Box m='auto' mt={2} maxWidth={600}>
        <AddNewProjectWrapper />
        <Grid container direction='column' justifyContent='center' alignItems='stretch'>
          {projects.map((project) => (
            <ProjectCardWrapper key={project.id} project={project} />
          ))}
        </Grid>
      </Box>
    </>
  )
}
