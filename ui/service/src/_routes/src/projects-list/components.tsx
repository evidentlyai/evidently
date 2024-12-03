import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import { AddNewProjectButton, ProjectCard } from 'evidently-ui-lib/components/ProjectCard'
import { useState } from 'react'
import { useSubmitFetcher } from '~/_routes/fetchers'

import { useOnSubmitEnd } from 'evidently-ui-lib/router-utils/hooks'
import { RouterLink } from '~/_routes/components'
import type { CurrentRoute } from './projects-list-main'

export const ProjectCardWrapper = ({ project }: { project: StrictID<ProjectModel> }) => {
  const projectFetcher = useSubmitFetcher<CurrentRoute>({
    actionPath: () => ({ path: '/?index', params: {} })
  })

  const [mode, setMode] = useState<'edit' | 'view'>('view')

  useOnSubmitEnd({
    state: projectFetcher.state,
    cb: () => {
      if (!(projectFetcher.data && 'error' in projectFetcher.data)) {
        setMode('view')
      }
    }
  })

  return (
    <ProjectCard
      LinkToProject={() => (
        <RouterLink
          type='link'
          title={project.name}
          to={'/:projectId'}
          paramsToReplace={{ projectId: project.id }}
          typographyProps={{ variant: 'h6' }}
        />
      )}
      project={project}
      mode={mode}
      onAlterMode={() => setMode((p) => (p === 'edit' ? 'view' : 'edit'))}
      disabled={projectFetcher.state !== 'idle'}
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

export const AddNewProjectWrapper = () => {
  const projectFetcher = useSubmitFetcher<CurrentRoute>({
    actionPath: () => ({ path: '/?index', params: {} })
  })

  const [opened, setOpened] = useState<boolean>(false)

  useOnSubmitEnd({
    state: projectFetcher.state,
    cb: () => {
      if (!(projectFetcher.data && 'error' in projectFetcher.data)) {
        setOpened(false)
      }
    }
  })

  return (
    <AddNewProjectButton
      disabled={projectFetcher.state !== 'idle'}
      opened={opened}
      alterOpened={() => setOpened((p) => !p)}
      onEditProject={(nameAndDescription) =>
        projectFetcher.submit({ action: 'create-project', project: nameAndDescription })
      }
    />
  )
}
