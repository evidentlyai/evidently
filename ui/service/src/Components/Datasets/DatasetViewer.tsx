import type { DatasetPaginationModel } from 'evidently-ui-lib/api/types'
import {
  DatasetViewerGeneral,
  type DatasetViewerGeneralProps
} from 'evidently-ui-lib/components/Datasets/Viewer/DatasetViewerGeneral'
import { useDatasetDataProps } from 'evidently-ui-lib/components/Datasets/hooks'
import type { DatasetParamsProps } from 'evidently-ui-lib/components/Datasets/types'
import { Toolbar } from './Toolbar'

type DatasetViewerProps = {
  datasetId: string
  data: DatasetPaginationModel
  datasetParams: DatasetParamsProps
} & Omit<
  DatasetViewerGeneralProps,
  'rows' | 'getRowId' | 'columns' | 'autoresizeColumns' | 'totalRowCount' | 'datasetParams'
>

export const DatasetViewer = (props: DatasetViewerProps) => {
  const { datasetId, data, datasetParams, ...restDatasetViewerGeneralProps } = props

  const { rows, getRowId, columns, autoresizeColumns, totalRowCount } = useDatasetDataProps(data)

  const { filters, setFilters, sortModel, clearFiltersAndSortModel } = datasetParams

  const toolbarComponentProps = {
    filters,
    setFilters,
    sortModel,
    clearFiltersAndSortModel,
    columns
  }

  return (
    <Toolbar.Context.Provider
      value={{
        toolbarComponentProps,
        downloadDatasetButtonProps: { datasetId }
      }}
    >
      <DatasetViewerGeneral
        rows={rows}
        columns={columns}
        autoresizeColumns={autoresizeColumns}
        totalRowCount={totalRowCount}
        getRowId={getRowId}
        datasetParams={datasetParams}
        {...restDatasetViewerGeneralProps}
        additionalSlots={{
          ...restDatasetViewerGeneralProps.additionalSlots,
          toolbar: Toolbar.Component
        }}
      />
    </Toolbar.Context.Provider>
  )
}
