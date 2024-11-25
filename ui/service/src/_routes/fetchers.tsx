import {
  type MatchWithAction,
  useSubmitFetcherGeneral
} from 'evidently-ui-lib/router-utils/fetchers'
import type { PathsWithDynamicSegments } from '~/_routes/types'

export const useSubmitFetcher = <K extends MatchWithAction>({
  providePath
}: {
  providePath: ({
    data
  }: { data: K['action']['args']['data'] }) => Extract<PathsWithDynamicSegments, K['path']>
}) => {
  return useSubmitFetcherGeneral<K, PathsWithDynamicSegments>({ providePath })
}
