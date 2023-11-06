import invariant from 'tiny-invariant'
import { ReportInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = ReportInfo[]

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.getReports(params.projectId)
  }
})
