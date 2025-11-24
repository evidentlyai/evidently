import { DataGrid, type GridColDef, type GridSlotsComponent, useGridApiRef } from '@mui/x-data-grid'
import type {
  DataGridPropsWithDefaultValues,
  DataGridPropsWithoutDefaultValue
} from '@mui/x-data-grid/models/props/DataGridProps'
import { useEffect } from 'react'
import type { DatasetParamsProps } from '~/components/Datasets/types'
import { addToPageNumber } from '~/components/Datasets/utils'

type AdditionalDataGridProps = Partial<
  Pick<
    DataGridPropsWithoutDefaultValue,
    'columnVisibilityModel' | 'onColumnVisibilityModelChange' | 'apiRef'
  >
> &
  Partial<Pick<DataGridPropsWithDefaultValues, 'autoHeight'>>

type EditableDataGridProps = Partial<
  Pick<
    DataGridPropsWithDefaultValues,
    'keepNonExistentRowsSelected' | 'checkboxSelection' | 'editMode'
  >
> &
  Partial<
    Pick<
      DataGridPropsWithoutDefaultValue,
      | 'processRowUpdate'
      | 'onCellEditStop'
      | 'onRowEditStop'
      | 'rowSelectionModel'
      | 'onRowSelectionModelChange'
    >
  >

export type DatasetViewerGeneralProps = {
  rows: Record<string, string>[]
  columns: GridColDef[]
  autoresizeColumns: string[]
  totalRowCount: number
  getRowId: (row: Record<string, string>) => string
  datasetParams: DatasetParamsProps
  isLoading: boolean
  additionalDataGridProps?: AdditionalDataGridProps
  editableDataGridProps?: EditableDataGridProps
  additionalSlots?: Partial<GridSlotsComponent>
  hideControls?: boolean
}

export const DatasetViewerGeneral = (props: DatasetViewerGeneralProps) => {
  const {
    rows,
    columns,
    autoresizeColumns,
    getRowId,
    totalRowCount,
    datasetParams,
    isLoading,
    additionalDataGridProps,
    editableDataGridProps,
    additionalSlots,
    hideControls
  } = props

  const { sortModel, setSortModeChange } = datasetParams

  // on server numeration starts from 1
  const paginationModel = addToPageNumber(datasetParams.paginationModel, -1)

  const setPaginationModel: (p: typeof paginationModel) => void = (paginationModel) =>
    datasetParams.setPaginationModel(addToPageNumber(paginationModel, 1))

  // Use internal apiRef if not provided
  const internalApiRef = useGridApiRef()
  const apiRef = additionalDataGridProps?.apiRef ?? internalApiRef

  const additionalDataGridPropsCustomized = {
    ...additionalDataGridProps,
    apiRef
  }

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (rows.length > 0 && autoresizeColumns.length > 0) {
      // Use setTimeout to ensure the grid is fully rendered
      const timer = setTimeout(() => {
        apiRef.current.autosizeColumns({
          columns: autoresizeColumns,
          includeHeaders: true,
          includeOutliers: true
        })
      }, 10)

      return () => clearTimeout(timer)
    }
  }, [])

  return (
    <>
      <DataGrid
        slots={{ ...additionalSlots, toolbar: hideControls ? undefined : additionalSlots?.toolbar }}
        slotProps={{
          toolbar: {
            printOptions: { disableToolbarButton: true },
            csvOptions: { disableToolbarButton: true }
          }
        }}
        {...additionalDataGridPropsCustomized}
        {...editableDataGridProps}
        columns={columns}
        rows={rows}
        getRowId={getRowId}
        disableColumnFilter
        getRowHeight={() => 'auto'}
        disableRowSelectionOnClick
        loading={isLoading}
        paginationMode='server'
        sortingMode='server'
        sortModel={sortModel}
        onSortModelChange={setSortModeChange}
        rowCount={totalRowCount}
        pageSizeOptions={[5, 10, 25, 50, 100]}
        paginationModel={paginationModel}
        onPaginationModelChange={setPaginationModel}
        {...(hideControls && { disableColumnSorting: true, hideFooter: true, density: 'compact' })}
        sx={{
          '& .MuiDataGrid-cell--flex': { display: 'block !important' },
          '&.MuiDataGrid-root--densityCompact .MuiDataGrid-cell': { py: '8px' },
          '&.MuiDataGrid-root--densityStandard .MuiDataGrid-cell': { py: '15px' },
          '&.MuiDataGrid-root--densityComfortable .MuiDataGrid-cell': { py: '22px' },
          '& .highlight-cell': { backgroundColor: 'divider' }
        }}
      />
    </>
  )
}
