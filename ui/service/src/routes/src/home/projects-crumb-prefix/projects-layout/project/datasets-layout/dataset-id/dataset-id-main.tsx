import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { PatchDatasetRequestModel } from 'evidently-ui-lib/api/types'
import { isSuccessData } from 'evidently-ui-lib/api/utils'
import { useDatasetParamsFromSearch } from 'evidently-ui-lib/components/Datasets/hooks'
import { getDatasetParamsForAPI } from 'evidently-ui-lib/components/Datasets/utils'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { ActionArgs, GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { DatasetViewer } from '~/Components/Datasets/DatasetViewer'
import { clientAPI } from '~/api'
import { redirect } from '~/routes/type-safe-route-helpers/utils'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/datasets/:datasetId'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

///////////////////
//    CRUMB
///////////////////
const crumb: CrumbDefinition = {
  keyFromLoaderData: 'datasetName' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = ({ params, searchParams }: loadDataArgs) => {
  const { datasetId: dataset_id } = params as Params

  const query = getDatasetParamsForAPI(searchParams)

  return clientAPI
    .GET('/api/datasets/{dataset_id}', {
      params: { path: { dataset_id }, query }
    })
    .then(responseParser())
    .then((datasetInfo) => ({ ...datasetInfo, datasetName: datasetInfo.metadata.name }))
}

///////////////////
//    ACTIONS
///////////////////
export const actions = {
  'delete-dataset': async (
    args: ActionArgs<{ data: { redirectOptions: { redirectTo: 'datasets' | 'no-redirect' } } }>
  ) => {
    const { data, params } = args

    const { datasetId: dataset_id, projectId } = params as Params

    const deleteResponse = await clientAPI
      .DELETE('/api/datasets/{dataset_id}', { params: { path: { dataset_id } } })
      .then(responseParser({ notThrowExc: true }))

    if (!isSuccessData(deleteResponse)) {
      return deleteResponse
    }

    if (data.redirectOptions.redirectTo === 'no-redirect') {
      return null
    }

    return redirect({
      to: `/projects/:projectId/${data.redirectOptions.redirectTo}`,
      paramsToReplace: { projectId }
    })
  },
  'update-dataset-metadata': async (args: ActionArgs<{ data: PatchDatasetRequestModel }>) => {
    const { data, params } = args
    const body = data

    const { datasetId: dataset_id } = params as Params

    return clientAPI.PATCH('/api/datasets/{dataset_id}', { params: { path: { dataset_id } }, body })
  }
}

export const Component = () => {
  const { loaderData: data, params, query, setQuery } = useCurrentRouteParams<CurrentRoute>()

  const { datasetId } = params

  const isLoading = useIsAnyLoaderOrActionRunning()

  const datasetParams = useDatasetParamsFromSearch({ query, setQuery, isLoading })

  return (
    <DatasetViewer
      isLoading={isLoading}
      datasetId={datasetId}
      data={data}
      datasetParams={datasetParams}
    />
  )
}
