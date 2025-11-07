import { JSONParseExtended } from 'evidently-ui-lib/api/JsonParser'
import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { DashboardInfoModel } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { useDatasetParamsFromSearch } from 'evidently-ui-lib/components/Datasets/hooks'
import { getDatasetParamsForAPI } from 'evidently-ui-lib/components/Datasets/utils'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { SnapshotViewWithDataset } from '~/Components/Snapshots/SnapshotViewWithDataset'
import { clientAPI } from '~/api'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/reports/:snapshotId'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

const crumb: CrumbDefinition = { param: 'snapshotId' satisfies keyof Params }

export const handle = { crumb }

export const loadData = async ({ params, searchParams }: loadDataArgs) => {
  const { projectId, snapshotId } = params as Params

  const snapshotPromise = clientAPI
    .GET('/api/projects/{project_id}/{snapshot_id}/data', {
      params: { path: { project_id: projectId, snapshot_id: snapshotId } },
      parseAs: 'text'
    })
    .then(responseParser())
    .then(JSONParseExtended<DashboardInfoModel>)

  const snapshotMetadata = await clientAPI
    .GET('/api/projects/{project_id}/{snapshot_id}/metadata', {
      params: { path: { project_id: projectId, snapshot_id: snapshotId } }
    })
    .then(responseParser())

  const linkedDatasetId = snapshotMetadata.links.datasets?.output?.current

  const linkedDatasetPromise = (() => {
    if (!linkedDatasetId) {
      return 'no_linking_dataset' as const
    }

    const query = getDatasetParamsForAPI(searchParams)

    return clientAPI
      .GET('/api/datasets/{dataset_id}', {
        params: { path: { dataset_id: linkedDatasetId }, query }
      })
      .then(responseParser({ notThrowExc: true }))
      .then((d) => ({ ...d, datasetId: linkedDatasetId }))
  })()

  const [snapshot, datasetData] = await Promise.all([snapshotPromise, linkedDatasetPromise])

  const linkedDatasetData = (() => {
    if (datasetData === 'no_linking_dataset') {
      return { type: 'no_linking_dataset' as const }
    }

    if (isSuccessData(datasetData)) {
      return { type: 'success' as const, datasetId: datasetData.datasetId, datasetData }
    }

    return { type: 'error' as const, error: datasetData.error }
  })()

  return { snapshot, linkedDatasetData }
}

export const Component = () => {
  const { loaderData, params, query, setQuery } = useCurrentRouteParams<CurrentRoute>()
  const { projectId, snapshotId } = params

  const { snapshot, linkedDatasetData } = loaderData

  const isLoading = useIsAnyLoaderOrActionRunning()
  const datasetParams = useDatasetParamsFromSearch({ query, setQuery, isLoading })

  return (
    <SnapshotViewWithDataset
      snapshot={snapshot}
      projectId={projectId}
      snapshotId={snapshotId}
      datasetParams={datasetParams}
      linkedDatasetData={linkedDatasetData}
      isLoading={isLoading}
    />
  )
}
