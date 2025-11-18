import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import { DatasetsTableV2 } from 'evidently-ui-lib/components/Datasets/Table/DatasetsTable'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { GetDatasetLinkByID } from '~/Components/Datasets/LinkToDataset'
import { clientAPI } from '~/api'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/datasets/?index'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type Params = GetParams<typeof currentRoutePath>

export const loadData = ({ params }: loadDataArgs) => {
  const { projectId } = params as Params

  return clientAPI
    .GET('/api/datasets', {
      params: { query: { project_id: projectId, origin: ['dataset', 'file'] } }
    })
    .then(responseParser())
}

export const Component = () => {
  const { loaderData, params } = useCurrentRouteParams<CurrentRoute>()

  const { datasets } = loaderData

  const { projectId } = params

  const isLoading = useIsAnyLoaderOrActionRunning()

  const deleteDatasetFetcher = useSubmitFetcher({
    path: '/projects/:projectId/datasets/:datasetId',
    action: 'delete-dataset'
  })

  const updateDatasetMetadataFetcher = useSubmitFetcher({
    path: '/projects/:projectId/datasets/:datasetId',
    action: 'update-dataset-metadata'
  })

  return (
    <DatasetsTableV2
      datasets={datasets}
      GetDatasetLinkByID={GetDatasetLinkByID}
      isLoading={isLoading}
      onUpdateMetadata={({ datasetId, data }) => {
        updateDatasetMetadataFetcher.submit({
          paramsToReplace: { projectId, datasetId },
          data
        })
      }}
      onDelete={(datasetId) => {
        if (confirm('Are you sure?') === true) {
          deleteDatasetFetcher.submit({
            data: { redirectOptions: { redirectTo: 'no-redirect' } },
            paramsToReplace: { projectId, datasetId }
          })
        }
      }}
    />
  )
}
