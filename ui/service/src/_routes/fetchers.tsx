import { useSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import type { MatchWithAction } from 'evidently-ui-lib/router-utils/types'
import type { PathsWithDynamicSegments } from '~/_routes/types'

export const useSubmitFetcher = <K extends MatchWithAction>({
  actionPath
}: {
  actionPath: ({
    data
  }: { data: K['action']['requestData'] }) => Extract<PathsWithDynamicSegments, K['path']>
}) => useSubmitFetcherGeneral<K>({ actionPath })
