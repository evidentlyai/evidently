import { ProjectInfo } from '~/api'
import { InJectAPI, expectJsonRequest } from '~/utils'

export type loaderData = ProjectInfo[]

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: () => api.getProjects(),
  action: async ({ request }) => {
    expectJsonRequest(request)

    const json = await request.json()
    return api.editProjectInfo(json)
  }
})
