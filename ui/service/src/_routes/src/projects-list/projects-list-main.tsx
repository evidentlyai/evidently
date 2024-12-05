import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import type { ActionSpecialArgs } from 'evidently-ui-lib/router-utils/types'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import {
  createProject,
  deleteProject,
  editProject,
  getProjects
} from 'evidently-ui-lib/routes-components/projectsList/data'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { assertNeverActionVariant } from 'evidently-ui-lib/utils/index'

import type { GetRouteByPath } from '~/_routes/types'

import { clientAPI } from '~/api'

import { useRouteParams } from 'evidently-ui-lib/router-utils/hooks'
import { AddNewProjectWrapper, ProjectCardWrapper } from './components'

///////////////////
//    ROUTE
///////////////////

type Path = '/?index'

export type CurrentRoute = GetRouteByPath<Path>

const crumb: CrumbDefinition = { title: 'Projects' }
export const handle = { crumb }

export const loaderSpecial = () => getProjects({ api: clientAPI })

type ActionRequestData =
  | { action: 'delete-project'; project_id: string }
  | { action: 'edit-project'; project: StrictID<ProjectModel> }
  | { action: 'create-project'; project: ProjectModel }

export const actionSpecial = async ({ data }: ActionSpecialArgs<{ data: ActionRequestData }>) => {
  const { action } = data

  if (action === 'delete-project') {
    return deleteProject({ api: clientAPI, project_id: data.project_id })
  }

  if (action === 'edit-project') {
    return editProject({ api: clientAPI, project: data.project })
  }

  if (action === 'create-project') {
    return createProject({ api: clientAPI, project: data.project })
  }

  assertNeverActionVariant(action)
}

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
