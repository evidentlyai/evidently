import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import { AddNewProjectButton, ProjectCard } from 'evidently-ui-lib/components/ProjectCard'
import { useState } from 'react'

import { createUseSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import { useOnSubmitEnd } from 'evidently-ui-lib/router-utils/hooks'
import { RouterLink } from '~/routes/components'
import type { CurrentRoute } from './projects-list-main'

const useFetcher = createUseSubmitFetcherGeneral<CurrentRoute>()

export const ProjectCardWrapper = ({ project }: { project: StrictID<ProjectModel> }) => {
  const [mode, setMode] = useState<'edit' | 'view'>('view')

  const deleteProjectFetcher = useFetcher({
    actionPath: () => ({ path: '/?index', params: {} }),
    action: 'delete-project'
  })

  useOnSubmitEnd({
    state: deleteProjectFetcher.state,
    cb: () => {
      if (!deleteProjectFetcher.data) {
        setMode('view')
      }
    }
  })

  const editProjectFetcher = useFetcher({
    actionPath: () => ({ path: '/?index', params: {} }),
    action: 'edit-project'
  })

  useOnSubmitEnd({
    state: editProjectFetcher.state,
    cb: () => {
      if (editProjectFetcher.data && !('error' in editProjectFetcher.data)) {
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
      onDeleteProject={(project_id) => deleteProjectFetcher.submit({ project_id })}
      onEditProject={(nameAndDescription) =>
        editProjectFetcher.submit({ project: { ...project, ...nameAndDescription } })
      }
    />
  )
}

const LinkToProject = ({ name, projectId }: { name: string; projectId: string }) => (
  <RouterLink
    type='link'
    variant='h6'
    title={name}
    to={'/:projectId'}
    paramsToReplace={{ projectId }}
  />
)

export const AddNewProjectWrapper = () => {
  const createProjectFetcher = useFetcher({
    actionPath: () => ({ path: '/?index', params: {} }),
    action: 'create-project'
  })

  const [opened, setOpened] = useState<boolean>(false)

  useOnSubmitEnd({
    state: createProjectFetcher.state,
    cb: () => {
      if (createProjectFetcher.data && !('error' in createProjectFetcher.data)) {
        setOpened(false)
      }
    }
  })

  return (
    <AddNewProjectButton
      disabled={createProjectFetcher.state !== 'idle'}
      opened={opened}
      alterOpened={() => setOpened((p) => !p)}
      onEditProject={(project) => createProjectFetcher.submit({ project })}
    />
  )
}
