import type { GridSortModel } from '@mui/x-data-grid'
import { JSONParseExtended } from '~/api/JsonParser'
import type { DatasetFilter } from '~/api/types'
import type { UpdatedCell } from '~/api/types'
import { isNotNull } from '~/utils'
import type { DatasetParamsData, PaginationModel } from './types'

export const EVIDENTLY_PROMPT_RESULT_COLUMN_NAME = '_evidently_prompt_result'

const DATASET_QUERY_PARAMS = {
  pagination_model: 'pagination_model',
  sort_model: 'sort_model',
  filters: 'filters'
} as const

type Row = Record<string, string>

export const getUpdatedRowsPoints = (old_row: Row, new_row: Row, rowId: string): UpdatedCell[] => {
  const notEqKeysWithNull = Object.keys(old_row).map((a_key) =>
    old_row?.[a_key] === new_row?.[a_key] ? null : a_key
  )

  const notEqKeys = notEqKeysWithNull.filter(isNotNull)

  const points: UpdatedCell[] = notEqKeys.map((column) => ({
    column,
    updated_value: new_row[column],
    row: Number(rowId)
  }))

  return points
}

export const addToPageNumber: (p: PaginationModel, add: number) => PaginationModel = (p, add) => ({
  ...p,
  page: p.page + add
})

export const getDatasetParamsFromSearch: (params?: URLSearchParams) => DatasetParamsData = (
  params = new URLSearchParams()
) => {
  const paginationModel: PaginationModel = (JSONParseExtended<PaginationModel>(
    params.get(DATASET_QUERY_PARAMS.pagination_model) ?? 'null'
  ) as PaginationModel | null) ?? {
    page: 1,
    pageSize: 10
  }

  const filters = JSONParseExtended<DatasetFilter[]>(
    params.get(DATASET_QUERY_PARAMS.filters) ?? '[]'
  )

  const sortModel: GridSortModel = JSONParseExtended<GridSortModel>(
    params.get(DATASET_QUERY_PARAMS.sort_model) ?? '[]'
  )

  return { paginationModel, filters, sortModel }
}

export const transformDatasetParamsToURLSearchParams = (params: Partial<DatasetParamsData>) => {
  const searchParams = new URLSearchParams(
    [
      params.filters ? [DATASET_QUERY_PARAMS.filters, JSON.stringify(params.filters)] : null,
      params.paginationModel
        ? [DATASET_QUERY_PARAMS.pagination_model, JSON.stringify(params.paginationModel)]
        : null,
      params.sortModel ? [DATASET_QUERY_PARAMS.sort_model, JSON.stringify(params.sortModel)] : null
    ].filter(isNotNull)
  )

  return searchParams
}

export const getDatasetParamsForAPI = (params: URLSearchParams) => {
  const { filters, sortModel, paginationModel } = getDatasetParamsFromSearch(params)

  const [sortElement] = sortModel

  return {
    page_size: paginationModel.pageSize,
    current_page: paginationModel.page,
    ...(sortElement
      ? {
          sort_by_column: sortElement.field,
          sort_ascending: sortElement.sort === 'asc'
        }
      : null),
    filters: filters.map((e) => JSON.stringify(e))
  }
}
