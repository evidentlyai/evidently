import invariant from 'tiny-invariant'
import { TestSuiteInfo } from '~/api'
import { InJectAPI } from '~/utils'

export type loaderData = TestSuiteInfo[]

export const injectAPI: InJectAPI<loaderData> = ({ api }) => ({
  loader: ({ params }) => {
    invariant(params.projectId, 'missing projectId')

    return api.getTestSuites(params.projectId)
  }
})
