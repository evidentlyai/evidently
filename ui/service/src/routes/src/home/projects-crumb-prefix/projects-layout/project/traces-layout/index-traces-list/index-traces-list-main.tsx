import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import type { DatasetModel } from 'evidently-ui-lib/api/types'
import { TracesTable } from 'evidently-ui-lib/components/Traces/TracesTable'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import invariant from 'tiny-invariant'
import { clientAPI } from '~/api'
import { useProjectInfo } from '~/contexts/project'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'
import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces/?index'

type CurrentRouteParams = GetParams<typeof currentRoutePath>
type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
///////////////////
//    LOADER
///////////////////

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params }: loadDataArgs) => {
  const { projectId } = params as CurrentRouteParams

  return clientAPI
    .GET('/api/datasets', { params: { query: { project_id: projectId, origin: ['tracing'] } } })
    .then(responseParser())
}

///////////////////
//  COMPONENT
///////////////////

export const Component = () => {
  const { loaderData, params } = useCurrentRouteParams<CurrentRoute>()

  const { datasets: traces } = loaderData

  const { projectId } = params

  const deleteDataset = useSubmitFetcher({
    path: '/projects/:projectId/datasets/:datasetId',
    action: 'delete-dataset'
  })

  const updateDatasetMetadataFetcher = useSubmitFetcher({
    path: '/projects/:projectId/datasets/:datasetId',
    action: 'update-dataset-metadata'
  })

  const isLoading = useIsAnyLoaderOrActionRunning()

  return (
    <TracesTable
      traces={traces}
      isLoading={isLoading}
      onUpdateMetadata={({ datasetId, data }) => {
        updateDatasetMetadataFetcher.submit({
          paramsToReplace: { projectId, datasetId },
          data
        })
      }}
      onDelete={(datasetId) => {
        if (confirm('Are you sure?') !== true) {
          return
        }

        deleteDataset.submit({
          data: { redirectOptions: { redirectTo: 'no-redirect' } },
          paramsToReplace: { projectId, datasetId }
        })
      }}
      GetDatasetLinkByID={GetTraceLinkByID}
    />
  )
}

const GetTraceLinkByID = ({ dataset }: { dataset: DatasetModel }) => {
  const { project } = useProjectInfo()
  invariant(project)

  const { id: projectId } = project
  const { id: datasetId } = dataset

  const isLoaing = useIsAnyLoaderOrActionRunning()

  return (
    <RouterLink
      type='button'
      disabled={isLoaing}
      title={'View'}
      to={'/projects/:projectId/traces/:exportId'}
      paramsToReplace={{ projectId, exportId: datasetId }}
    />
  )
}
