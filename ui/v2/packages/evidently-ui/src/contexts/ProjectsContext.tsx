import React from 'react'

import { ProjectInfo } from '../api'

export interface ProjectsContextState {
  Projects: ProjectInfo[]
  CurrentProjectId?: string
  ChangeProject?: (projectId: string) => void
  ChangeSection?: (projectId: string, sections: string[]) => void
}

const ProjectsContext = React.createContext<ProjectsContextState>({
  Projects: []
})

export default ProjectsContext
