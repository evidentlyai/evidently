import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import { ensureIDInArray } from 'evidently-ui-lib/api/utils'
import { useCurrentRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import type { ActionArgs } from 'evidently-ui-lib/router-utils/types'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'
import { AddNewProjectWrapper, ProjectCardWrapper } from './components'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/?index'
export type CurrentRoute = GetRouteByPath<typeof currentRoutePath>

export const loadData = () =>
  clientAPI.GET('/api/projects').then(responseParser()).then(ensureIDInArray)

export const actions = {
  'delete-project': (args: ActionArgs<{ data: { project_id: string } }>) =>
    clientAPI
      .DELETE('/api/v2/projects/{project_id}', {
        params: { path: { project_id: args.data.project_id } }
      })
      .then(responseParser({ notThrowExc: true })),
  'create-project': ({ data }: ActionArgs<{ data: { project: ProjectModel } }>) =>
    clientAPI
      .POST('/api/v2/projects', { body: data.project })
      .then(responseParser({ notThrowExc: true })),
  'edit-project': (args: ActionArgs<{ data: { project: StrictID<ProjectModel> } }>) =>
    clientAPI
      .POST('/api/projects/{project_id}/info', {
        params: { path: { project_id: args.data.project.id } },
        body: args.data.project
      })
      .then(responseParser({ notThrowExc: true }))
}

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
