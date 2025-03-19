import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import { AddNewProjectButton, ProjectCard } from 'evidently-ui-lib/components/ProjectCard'
import { useState } from 'react'

import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { useOnSubmitEnd } from 'evidently-ui-lib/router-utils/hooks'
import { RouterLink } from '~/routes/components'
import { useSubmitFetcher } from '~/routes/hooks'

export const ProjectCardWrapper = ({ project }: { project: StrictID<ProjectModel> }) => {
  const [mode, setMode] = useState<'edit' | 'view'>('view')

  const deleteProjectFetcher = useSubmitFetcher({
    path: '/?index',
    action: 'delete-project'
  })

  useOnSubmitEnd({
    state: deleteProjectFetcher.state,
    cb: () => {
      if (isSuccessData(deleteProjectFetcher.data)) {
        setMode('view')
      }
    }
  })

  const editProjectFetcher = useSubmitFetcher({
    path: '/?index',
    action: 'edit-project'
  })

  useOnSubmitEnd({
    state: editProjectFetcher.state,
    cb: () => {
      if (isSuccessData(editProjectFetcher.data)) {
        setMode('view')
      }
    }
  })

  return (
    <ProjectCard
      LinkToProject={LinkToProject}
      project={project}
      mode={mode}
      onAlterMode={() => setMode((p) => (p === 'edit' ? 'view' : 'edit'))}
      disabled={deleteProjectFetcher.state !== 'idle'}
      onDeleteProject={(project_id) => deleteProjectFetcher.submit({ data: { project_id } })}
      onEditProject={(nameAndDescription) =>
        editProjectFetcher.submit({ data: { project: { ...project, ...nameAndDescription } } })
      }
    />
  )
}

const LinkToProject = ({ name, projectId }: { name: string; projectId: string }) => (
  <RouterLink
    type='link'
    variant='h6'
    title={name}
    to={'/projects/:projectId'}
    paramsToReplace={{ projectId }}
  />
)

export const AddNewProjectWrapper = () => {
  const createProjectFetcher = useSubmitFetcher({
    path: '/?index',
    action: 'create-project'
  })

  const [opened, setOpened] = useState<boolean>(false)

  useOnSubmitEnd({
    state: createProjectFetcher.state,
    cb: () => {
      if (isSuccessData(createProjectFetcher.data)) {
        setOpened(false)
      }
    }
  })

  return (
    <AddNewProjectButton
      disabled={createProjectFetcher.state !== 'idle'}
      opened={opened}
      alterOpened={() => setOpened((p) => !p)}
      onEditProject={(project) => createProjectFetcher.submit({ data: { project } })}
    />
  )
}
