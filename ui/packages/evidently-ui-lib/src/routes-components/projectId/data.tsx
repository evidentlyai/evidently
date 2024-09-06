import invariant from 'tiny-invariant'
import { type API_CLIENT_TYPE, responseParser } from '~/api/client-heplers'
import type { ProjectModel } from '~/api/types'
import type { StrictID } from '~/api/types/utils'
import { type GetLoaderAction, ensureID } from '~/api/utils'

export type LoaderData = StrictID<ProjectModel>

export const getLoaderAction: GetLoaderAction<API_CLIENT_TYPE, LoaderData> = ({ api }) => ({
  loader: ({ params }) => {
    const { projectId } = params
    invariant(projectId, 'missing projectId')

    return api
      .GET('/api/projects/{project_id}/info', { params: { path: { project_id: projectId } } })
      .then(responseParser())
      .then(ensureID)
  }
})
