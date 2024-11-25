import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import { AddNewProjectButton, ProjectCard } from 'evidently-ui-lib/components/ProjectCard'
import {
  deleteProject,
  editProject,
  getProjects
} from 'evidently-ui-lib/routes-components/projectsList/data'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { LoaderFunctionArgs } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { assertNeverActionVariant } from 'evidently-ui-lib/utils/index'
import { useState } from 'react'
import { useSubmitFetcher } from '~/_routes/fetchers'
import { useIsAnyLoaderOrActionRunning, useOnSubmitEnd, useRouteParams } from '~/_routes/hooks'
import type { ActionSpecialArgs, GetRouteByPath } from '~/_routes/types'
import type { CrumbDefinition } from '~/_routes/utils'
import { clientAPI } from '~/api'

///////////////////
//    ROUTE
///////////////////

export type Route = GetRouteByPath<'/?index'>

const crumb: CrumbDefinition = { title: 'Projects' }

export const handle = { crumb }

export const loader = (_args: LoaderFunctionArgs) => getProjects({ api: clientAPI })

type ActionRequestData =
  | { action: 'delete-project'; project_id: string }
  | { action: 'edit-project'; project: StrictID<ProjectModel> }

export const actionSpecial = async ({ data }: ActionSpecialArgs<{ data: ActionRequestData }>) => {
  console.log('123', data)

  const { action } = data

  if (action === 'delete-project') {
    return deleteProject({ api: clientAPI, project_id: data.project_id })
  }

  if (action === 'edit-project') {
    return editProject({ api: clientAPI, project: data.project })
  }

  assertNeverActionVariant(action)
}

const ProjectCardWrapper = ({ project }: { project: StrictID<ProjectModel> }) => {
  const projectFetcher = useSubmitFetcher<Route>({ providePath: () => '/?index' })

  const [mode, setMode] = useState<'edit' | 'view'>('view')

  useOnSubmitEnd({
    state: projectFetcher.state,
    cb: () => projectFetcher.data === null && setMode('view')
  })

  const disabled = useIsAnyLoaderOrActionRunning()

  return (
    <ProjectCard
      project={project}
      mode={mode}
      onAlterMode={() => setMode((p) => (p === 'edit' ? 'view' : 'edit'))}
      disabled={disabled}
      onDeleteProject={(project_id) =>
        projectFetcher.submit({ action: 'delete-project', project_id })
      }
      onEditProject={(nameAndDescription) =>
        projectFetcher.submit({
          action: 'edit-project',
          project: { ...project, ...nameAndDescription }
        })
      }
    />
  )
}

export const Component = () => {
  const { loaderData: projects } = useRouteParams<Route>()

  return (
    <>
      <Typography align='center' variant='h5'>
        {projects.length > 0 ? 'Project List' : "You don't have any projects yet"}
      </Typography>
      <Box m='auto' mt={2} maxWidth={600}>
        <AddNewProjectButton />
        <Grid container direction='column' justifyContent='center' alignItems='stretch'>
          {projects.map((project) => (
            <ProjectCardWrapper key={project.id} project={project} />
          ))}
        </Grid>
      </Box>
    </>
  )
}
