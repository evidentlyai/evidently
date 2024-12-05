import { useSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import type { GetParams, MatchWithAction } from 'evidently-ui-lib/router-utils/types'
import { replaceParamsInLink } from 'evidently-ui-lib/router-utils/utils'

export const useSubmitFetcher = <K extends MatchWithAction>({
  actionPath
}: {
  actionPath: ({ data }: { data: K['action']['requestData'] }) => {
    path: K['path']
    params: GetParams<K['path']>
  }
}) => {
  return useSubmitFetcherGeneral<K>({
    actionPath: (...args) => {
      const { path, params } = actionPath(...args)

      return replaceParamsInLink(params, path)
    }
  })
}
