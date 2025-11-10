import { Box, Stack } from '@mui/material'
import {
  type GridColDef,
  type GridSlotProps,
  type GridSortModel,
  GridToolbar
} from '@mui/x-data-grid'
import type { DatasetFilter } from '~/api/types'
import { FilterCompoent } from './Components/FilterPopover'
import { ResetDatasetSettingsButton } from './Components/ResetDatasetSettings'

export type CustomDatasetToolbarComponentProps = {
  filters: DatasetFilter[]
  setFilters: (filters: DatasetFilter[]) => void
  sortModel: GridSortModel
  clearFiltersAndSortModel: () => void
  columns: GridColDef[]
}

export type CustomDatasetToolbarProps = {
  standartGridToolbarProps: GridSlotProps['toolbar']
  toolbarComponentProps: CustomDatasetToolbarComponentProps
  slotOne?: React.ReactNode
  slotTwo?: React.ReactNode
}

export const CustomDatasetToolbar = (props: CustomDatasetToolbarProps) => {
  const { standartGridToolbarProps, toolbarComponentProps, slotOne, slotTwo } = props

  const { columns, filters, setFilters, clearFiltersAndSortModel, sortModel } =
    toolbarComponentProps

  const isFilteringOrSorting = filters.length > 0 || sortModel.length > 0

  return (
    <Stack direction={'row'} alignItems={'center'} gap={1} p={0.5}>
      <FilterCompoent filters={filters} setFilters={setFilters} columns={columns} />

      <Box flexGrow={1}>
        <Stack direction={'row'} alignItems={'center'} gap={0}>
          <GridToolbar {...standartGridToolbarProps} sx={{ p: 0 }} />
          {slotOne}
        </Stack>
      </Box>

      {slotTwo}

      <ResetDatasetSettingsButton
        isFilteringOrSorting={isFilteringOrSorting}
        clearFiltersAndSortModel={clearFiltersAndSortModel}
      />
    </Stack>
  )
}
