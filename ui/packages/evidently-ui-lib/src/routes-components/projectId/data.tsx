import invariant from 'tiny-invariant'
import { ProjectModel } from '~/api/types'
import { ProjectsProvider } from '~/api/types/providers/projects'
import { StrictID } from '~/api/types/utils'
import { GetLoaderAction } from '~/api/utils'

export type LoaderData = StrictID<ProjectModel>

export const getLoaderAction: GetLoaderAction<ProjectsProvider, LoaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId } = params
    invariant(projectId, 'missing projectId')

    return api.get({ id: projectId })
  }
})
