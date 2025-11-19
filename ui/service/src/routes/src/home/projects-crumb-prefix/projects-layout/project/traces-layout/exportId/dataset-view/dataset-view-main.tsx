import { responseParser } from 'evidently-ui-lib/api/client-heplers'
import {
  useColumnVisibilityModelHidingTokensAndCostColumns,
  useDatasetParamsFromSearch
} from 'evidently-ui-lib/components/Datasets/hooks'
import { getDatasetParamsForAPI } from 'evidently-ui-lib/components/Datasets/utils'
import { NameAndDescriptionPopover } from 'evidently-ui-lib/components/Utils/NameAndDescriptionForm'
import { useTraceToolbarRef } from 'evidently-ui-lib/contexts/TraceToolbarContext'
import {
  useCurrentRouteParams,
  useIsAnyLoaderOrActionRunning
} from 'evidently-ui-lib/router-utils/hooks'
import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/router-builder'
import type { GetParams, loadDataArgs } from 'evidently-ui-lib/router-utils/types'
import { Portal } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { DatasetViewer } from '~/Components/Datasets/DatasetViewer'
import { clientAPI } from '~/api'
import { useSubmitFetcher } from '~/routes/type-safe-route-helpers/hooks'

import type { GetRouteByPath } from '~/routes/types'

///////////////////
//    ROUTE
///////////////////

export const currentRoutePath = '/projects/:projectId/traces/:exportId/dataset'

type CurrentRoute = GetRouteByPath<typeof currentRoutePath>
type CurrentRouteParams = GetParams<typeof currentRoutePath>
///////////////////
//    CRUMB
///////////////////

const crumb: CrumbDefinition = {
  keyFromLoaderData: 'name' satisfies keyof CurrentRoute['loader']['returnType']
}

export const handle = { crumb }

///////////////////
//    LOADER
///////////////////
export const loadData = async ({ params, searchParams }: loadDataArgs) => {
  const query = getDatasetParamsForAPI(searchParams)

  const { exportId } = params as CurrentRouteParams

  return clientAPI
    .GET('/api/datasets/{dataset_id}', {
      params: { path: { dataset_id: exportId }, query }
    })
    .then(responseParser())
    .then((data) => ({ ...data, name: data.metadata.name }))
}

///////////////////
//  COMPONENT
///////////////////

export const Component = () => {
  const { loaderData: data, query, setQuery, params } = useCurrentRouteParams<CurrentRoute>()

  const { exportId, projectId } = params

  const isLoading = useIsAnyLoaderOrActionRunning()

  const datasetParams = useDatasetParamsFromSearch({ query, setQuery, isLoading })

  const [columnVisibilityModel, onColumnVisibilityModelChange] =
    useColumnVisibilityModelHidingTokensAndCostColumns(data.metadata.columns.map((col) => col.name))

  const exportToDatasetFetcher = useSubmitFetcher({
    path: '/projects/:projectId/datasets',
    action: 'export-to-dataset-from-source-and-redirect-to-dataset'
  })

  const traceToolbarRef = useTraceToolbarRef()

  return (
    <>
      <Portal container={() => traceToolbarRef.current}>
        <NameAndDescriptionPopover
          formProps={{
            allowSubmitDefaults: true,
            submitButtonTitle: 'Submit',
            defaultValues: { name: `Export of ${data.name}` },
            isLoading: exportToDatasetFetcher.state !== 'idle',
            onSubmit: ({ name, description }) => {
              exportToDatasetFetcher.submit({
                data: {
                  name,
                  description,
                  source: {
                    type: 'evidently:data_source_dto:TracingDataSourceDTO',
                    export_id: exportId
                  }
                },
                paramsToReplace: { projectId }
              })
            }
          }}
          buttonTitle='Export to Dataset'
        />
      </Portal>

      <DatasetViewer
        data={data}
        datasetId={exportId}
        isLoading={isLoading}
        datasetParams={datasetParams}
        additionalDataGridProps={{
          autoHeight: true,
          columnVisibilityModel,
          onColumnVisibilityModelChange
        }}
      />
    </>
  )
}
