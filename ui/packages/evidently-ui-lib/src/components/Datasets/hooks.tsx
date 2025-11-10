import { Box, InputBase, type InputBaseProps } from '@mui/material'
import {
  type GridColDef,
  type GridRenderCellParams,
  type GridRenderEditCellParams,
  type GridSortModel,
  useGridApiContext
} from '@mui/x-data-grid'
import dayjs from 'dayjs'
import { useCallback, useLayoutEffect, useMemo, useState } from 'react'
import type { DatasetFilter, DatasetPaginationModel } from '~/api/types'
import { useStableCallbackWithLatestScope } from '~/hooks'
import type { RouteQueryParams } from '~/router-utils/hooks'
import { assertNever, isNotNull } from '~/utils'
import type { DatasetParamsProps, PaginationModel } from './types'
import { EVIDENTLY_PROMPT_RESULT_COLUMN_NAME } from './utils'
import { getDatasetParamsFromSearch, transformDatasetParamsToURLSearchParams } from './utils'

type ColumnRaw = GridColDef & {
  isIndex: boolean
  autoResizable: boolean
  specialType:
    | 'link_to_trace'
    | 'human_feedback_label'
    | 'human_feedback_comment'
    | 'prompt_result'
    | null
}

export const useDatasetDataProps = (data: DatasetPaginationModel, isEditable?: boolean) => {
  const columnsRaw: ColumnRaw[] = useMemo(
    () =>
      data.metadata.columns.map((column, columnIndex) => {
        const columnType = column.type
        const header = column.name
        const isIndex = column.is_index
        const isColumnBig = data.items.some((e) => String(e?.[columnIndex] ?? '').length > 50)

        const specialType = (() => {
          const serviceColumns = data.metadata.data_definition?.service_columns

          if (
            (serviceColumns?.trace_link && header === serviceColumns.trace_link) ||
            header === LINK_TO_TRACE_COLUMN_NAME
          ) {
            return 'link_to_trace'
          }

          if (
            serviceColumns?.human_feedback_label &&
            header === serviceColumns.human_feedback_label
          ) {
            return 'human_feedback_label'
          }

          if (
            serviceColumns?.human_feedback_comment &&
            header === serviceColumns.human_feedback_comment
          ) {
            return 'human_feedback_comment'
          }

          if (header.includes(EVIDENTLY_PROMPT_RESULT_COLUMN_NAME)) {
            return 'prompt_result'
          }

          return null
        })()

        const width = specialType === 'link_to_trace' ? 200 : isColumnBig ? 500 : 100

        const autoResizable = !isColumnBig

        const headerName = (() => {
          if (specialType === 'prompt_result') {
            return `✨ ${header.replaceAll(EVIDENTLY_PROMPT_RESULT_COLUMN_NAME, '')}`
          }

          if (specialType === 'link_to_trace') {
            return '🔗 evidently trace link'
          }

          return header
        })()

        const editable = isIndex ? false : isEditable

        const type = (() => {
          if (
            (specialType === 'link_to_trace' ||
              specialType === 'human_feedback_label' ||
              specialType === 'human_feedback_comment') &&
            !isEditable
          ) {
            return 'actions'
          }

          if (columnType === 'string') {
            return 'string'
          }

          if (columnType === 'datetime') {
            return 'dateTime'
          }

          if (columnType === 'numerical') {
            return 'number'
          }

          return assertNever(columnType)
        })()

        return {
          isIndex: isIndex ?? false,
          width,
          autoResizable,
          specialType,
          field: header,
          headerName,
          editable,
          type,
          renderCell: (params) => <RenderCell {...params} />,
          ...(columnType === 'string' && {
            renderEditCell: (params) => <EditTextarea {...params} />
          }),
          ...(specialType === 'prompt_result' && { cellClassName: 'highlight-cell' }),
          ...(columnType === 'datetime' && {
            valueFormatter: (value) =>
              dayjs(value).locale('en-gb').format('ddd, MMM D, YYYY h:mm:ss A')
          })
        }
      }),
    [data, isEditable]
  )

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  const columns = useMemo(() => columnsRaw, [JSON.stringify(columnsRaw)])

  const columnsWithoutIndex = useMemo(() => columns.filter((e) => !e.isIndex), [columns])

  const autoresizeColumns = useMemo(
    () => columnsWithoutIndex.filter((e) => e.autoResizable).map((e) => e.field),
    [columnsWithoutIndex]
  )

  const rows: Record<string, string>[] = useMemo(
    () =>
      data.items.map((row, rowIndex) =>
        columns.reduce(
          (r, column, index) => {
            // @ts-ignore
            r[column.field] = row[index]
            return r
          },
          { _evidently_row_index: String(rowIndex) }
        )
      ),
    [data, columns]
  )

  const getRowIdGeneratedOnFront = useCallback(
    (r: Record<string, string>) => r._evidently_row_index,
    []
  )

  const indexColumnName = columns.find((e) => e.isIndex)?.headerName

  const indexColumn = useMemo(
    () => columns.find((e) => e.headerName === indexColumnName),
    [columns, indexColumnName]
  )

  const getRowIdByIndexColumn = useCallback(
    (row: Record<string, string>) => {
      if (!indexColumn) {
        return ''
      }

      return row[indexColumn.field] ?? ''
    },
    [indexColumn]
  )

  const getRowId = indexColumnName ? getRowIdByIndexColumn : getRowIdGeneratedOnFront

  const totalRowCount = data.metadata.row_count

  return {
    columns: columnsWithoutIndex,
    autoresizeColumns,
    getRowId,
    rows,
    totalRowCount
  }
}

export type UseDatasetParamsFromSearchProps = Pick<RouteQueryParams, 'setQuery' | 'query'> & {
  isLoading: boolean
}

export const useDatasetParamsFromSearch = (
  params: UseDatasetParamsFromSearchProps
): DatasetParamsProps => {
  const { setQuery, query, isLoading } = params

  const searchParams = new URLSearchParams(
    Object.entries(query)
      .map(([k, v]) => (v ? [k, v] : null))
      .filter(isNotNull)
  )

  const datasetParams = getDatasetParamsFromSearch(searchParams)

  const setPaginationModel = useStableCallbackWithLatestScope(
    (paginationModel: PaginationModel) => {
      if (isLoading) {
        return
      }

      setQuery(
        Object.fromEntries(transformDatasetParamsToURLSearchParams({ paginationModel })),
        NAVIGATE_OPTIONS
      )
    }
  )

  const setFilters = useStableCallbackWithLatestScope((filters: DatasetFilter[]) => {
    if (isLoading) {
      return
    }

    setQuery(
      Object.fromEntries(transformDatasetParamsToURLSearchParams({ filters })),
      NAVIGATE_OPTIONS
    )
  })

  const clearFiltersAndSortModel = useStableCallbackWithLatestScope(() => {
    if (isLoading) {
      return
    }

    setQuery(
      Object.fromEntries(transformDatasetParamsToURLSearchParams({ filters: [], sortModel: [] })),
      NAVIGATE_OPTIONS
    )
  })

  const setSortModeChange = useStableCallbackWithLatestScope((sortModel: GridSortModel) => {
    if (isLoading) {
      return
    }

    setQuery(
      Object.fromEntries(transformDatasetParamsToURLSearchParams({ sortModel })),
      NAVIGATE_OPTIONS
    )
  })

  return {
    ...datasetParams,
    setPaginationModel,
    setSortModeChange,
    setFilters,
    clearFiltersAndSortModel
  }
}

const EditTextarea = (
  props: GridRenderEditCellParams<
    // biome-ignore lint/suspicious/noExplicitAny: fine
    any,
    string
  >
) => {
  const { id, field, value, hasFocus } = props

  const [inputRef, setInputRef] = useState<HTMLInputElement | null>(null)
  const apiRef = useGridApiContext()

  useLayoutEffect(() => {
    if (hasFocus && inputRef) {
      inputRef.focus()
    }
  }, [hasFocus, inputRef])

  const handleChange = useCallback<NonNullable<InputBaseProps['onChange']>>(
    (event) => {
      const newValue = event.target.value

      apiRef.current.setEditCellValue({ id, field, value: newValue }, event)
    },
    [apiRef, field, id]
  )

  return (
    <InputBase
      sx={{ fontSize: 'inherit', display: 'unset', px: '10px', pt: '2px' }}
      multiline
      value={value}
      fullWidth
      onChange={handleChange}
      inputRef={(ref) => setInputRef(ref)}
    />
  )
}

type RenderCellProps = GridRenderCellParams

export const RenderCell = (props: RenderCellProps) => {
  const stringValue = String(props.value)

  return <Box sx={{ maxHeight: 500, overflow: 'auto', whiteSpace: 'pre-wrap' }}>{stringValue}</Box>
}

const NAVIGATE_OPTIONS = { replace: true, preventScrollReset: true } as const
const LINK_TO_TRACE_COLUMN_NAME = '_evidently_trace_link'
