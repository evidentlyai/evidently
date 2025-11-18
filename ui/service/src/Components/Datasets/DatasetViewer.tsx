import type { DatasetPaginationModel } from 'evidently-ui-lib/api/types'
import {
  DatasetViewerGeneral,
  type DatasetViewerGeneralProps
} from 'evidently-ui-lib/components/Datasets/Viewer/DatasetViewerGeneral'
import { useDatasetDataProps } from 'evidently-ui-lib/components/Datasets/hooks'
import type { DatasetParamsProps } from 'evidently-ui-lib/components/Datasets/types'
import type { GridColDef } from 'evidently-ui-lib/shared-dependencies/mui-x-date-grid'
import { useMemo } from 'react'
import { RenderCell } from '~/Components/Datasets/RenderCell'
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

  const {
    rows,
    getRowId,
    columns: _columns,
    autoresizeColumns,
    totalRowCount
  } = useDatasetDataProps(data)

  // custom Render cell method
  const columns: GridColDef[] = useMemo(
    () =>
      _columns.map((column) => ({
        ...column,
        renderCell: (params) => <RenderCell specialColumnType={column.specialType} {...params} />
      })),
    [_columns]
  )

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
      value={{ toolbarComponentProps, downloadDatasetButtonProps: { datasetId } }}
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
