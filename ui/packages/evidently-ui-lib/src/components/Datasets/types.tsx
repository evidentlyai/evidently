import type { GridSortModel } from '@mui/x-data-grid'
import type { DatasetFilter } from '~/api/types'

export type PaginationModel = { page: number; pageSize: number }

export type DatasetParamsProps = {
  paginationModel: PaginationModel
  setPaginationModel: (pageModel: PaginationModel) => void
  sortModel: GridSortModel
  setSortModeChange: (sortModel: GridSortModel) => void
  filters: DatasetFilter[]
  setFilters: (filters: DatasetFilter[]) => void
  clearFiltersAndSortModel: () => void
}

export type DatasetParamsData = Pick<
  DatasetParamsProps,
  'filters' | 'paginationModel' | 'sortModel'
>
