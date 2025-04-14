import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import {
  getProjects,
  getProjectsListActions
} from 'evidently-ui-lib/routes-components/projectsList/data'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'

import type { GetRouteByPath } from '~/routes/types'

import { clientAPI } from '~/api'

import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { AddNewProjectWrapper, ProjectCardWrapper } from './components'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/?index'
export type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

const crumb: CrumbDefinition = { title: 'Projects' }
export const handle = { crumb }

export const loadData = () => getProjects({ api: clientAPI })

export const actions = getProjectsListActions({ api: clientAPI })

export const Component = () => {
  const { loaderData: projects } = useCurrentRouteParams<CurrentRoute>()

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
