import type { ProjectModel } from 'evidently-ui-lib/api/types'
import type { StrictID } from 'evidently-ui-lib/api/types/utils'
import React from 'react'

export const ProjectContext = React.createContext<{ project: StrictID<ProjectModel> | null }>({
  project: null
})

export const useProjectInfo = () => React.useContext(ProjectContext)
