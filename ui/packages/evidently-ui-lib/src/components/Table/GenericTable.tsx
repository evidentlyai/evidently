import { Grade as GradeIcon } from '@mui/icons-material'
import { GradeOutlined as GradeOutlinedIcon } from '@mui/icons-material'
import {
  Box,
  IconButton,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableSortLabel,
  Typography,
  tableCellClasses
} from '@mui/material'
import { useEffect, useMemo, useState } from 'react'
import { useLocalStorage } from '~/hooks/index'

const DARK_CELL_BACKGROUND = '#171717'
const LIGHT_CELL_BACKGROUND = '#f5f5f5'
const FAVOURITE_BUTTON_CLASS_NAME = 'action-buttons'

export interface TableColumn<T> {
  key: string
  label: string
  sortable?: {
    getSortValue: (item: T) => string | number | Date | undefined | null
    isDateString?: boolean
  }
  render: (item: T) => React.ReactNode
  skipRender?: boolean
  align?: 'left' | 'center' | 'right'
  sticky?: boolean

  minWidth?: number | string
  maxWidth?: number | string
}

export interface FavoritesConfig {
  enabled: boolean
  storageKey: string
}

export interface TableProps<T> {
  data: T[]
  columns: TableColumn<T>[]
  idField: keyof T
  selectedRowId?: string | null
  emptyMessage?: React.ReactNode
  favorites?: FavoritesConfig
  defaultSort?: {
    column: string
    direction: 'asc' | 'desc'
  }
  tableSize?: 'small' | 'medium'
  enableOverflowScroll?: boolean
  isLoading?: boolean
  removeLastBorderBottom?: boolean
  stickyDarkCellBackgroundColor?: string
}

export function GenericTable<T extends Record<string, unknown>>(props: TableProps<T>) {
  const {
    data,
    columns,
    idField,
    favorites,
    defaultSort,
    emptyMessage = "You don't have any data yet.",
    tableSize = 'small',
    enableOverflowScroll = false,
    isLoading = false,
    selectedRowId,
    removeLastBorderBottom = false,
    stickyDarkCellBackgroundColor = DARK_CELL_BACKGROUND
  } = props

  const [sortState, setSortState] = useState<{
    column: string
    sortType: 'desc' | 'asc' | undefined
  }>({
    column: defaultSort?.column || '',
    sortType: defaultSort?.direction || 'desc'
  })

  const [favoriteIds, setFavoriteIds] = useLocalStorage<string[]>(
    favorites?.storageKey || 'favorite-ids',
    []
  )

  // Clean up old favorites
  useEffect(() => {
    if (favorites?.enabled && favoriteIds.length > 150) {
      setFavoriteIds((prev) => prev.slice(50))
    }
  }, [favoriteIds, favorites?.enabled, setFavoriteIds])

  const sortedData = useMemo(() => {
    let result = [...data]

    // Apply sorting if enabled
    if (sortState.sortType && sortState.column) {
      const column = columns.find((col) => col.key === sortState.column)
      if (column?.sortable?.getSortValue) {
        result = result.toSorted((a, b) => {
          const aValue = column?.sortable?.getSortValue?.(a)
          const bValue = column?.sortable?.getSortValue?.(b)

          let diff = 0

          // Handle different data types
          if (typeof aValue === 'string' && typeof bValue === 'string') {
            // For date strings, try to parse them
            if (column.sortable?.isDateString) {
              diff = Date.parse(aValue) - Date.parse(bValue)
            } else {
              diff = bValue.localeCompare(aValue)
            }
          } else if (typeof aValue === 'number' && typeof bValue === 'number') {
            diff = aValue - bValue
          }

          return sortState.sortType === 'desc' ? -diff : diff
        })
      }
    }

    // Apply favorites sorting if enabled
    if (favorites?.enabled) {
      result = result.toSorted((a, b) => {
        const aId = String(a[idField as string])
        const bId = String(b[idField as string])

        const aInFavorite = favoriteIds.includes(aId) ? 1 : 0
        const bInFavorite = favoriteIds.includes(bId) ? 1 : 0

        return bInFavorite - aInFavorite
      })
    }

    return result
  }, [data, sortState, columns, favoriteIds, favorites, idField])

  const handleSortClick = (column: TableColumn<T>) => () => {
    if (!column.sortable) return

    setSortState((prev) => ({
      column: column.key,
      sortType:
        prev.sortType === undefined
          ? 'desc'
          : prev.sortType === 'desc'
            ? 'asc'
            : prev.column === column.key
              ? undefined
              : 'desc'
    }))
  }

  const isSortActive = (column: TableColumn<T>) =>
    Boolean(sortState.column === column.key && sortState.sortType)

  const getSortDirection = (column: TableColumn<T>) =>
    sortState.column === column.key ? sortState.sortType : undefined

  const toggleFavorite = (item: T) => {
    if (!favorites?.enabled) {
      return
    }

    const itemId = String(item[idField as string])

    setFavoriteIds((prev) => {
      if (prev.includes(itemId)) {
        return prev.filter((id) => id !== itemId)
      }

      return [...prev, itemId]
    })
  }

  const isFavorite = (item: T) => {
    if (!favorites?.enabled) {
      return false
    }

    const itemId = String(item[idField as string])
    return favoriteIds.includes(itemId)
  }

  const renderFavoriteButton = (item: T) => {
    if (!favorites?.enabled) return null

    return (
      <IconButton
        disabled={isLoading}
        className={FAVOURITE_BUTTON_CLASS_NAME}
        sx={{
          opacity: 0,
          transition: (theme) =>
            theme.transitions.create('opacity', {
              duration: theme.transitions.duration.enteringScreen
            })
        }}
        onClick={() => toggleFavorite(item)}
      >
        {isFavorite(item) ? <GradeIcon /> : <GradeOutlinedIcon />}
      </IconButton>
    )
  }

  if (sortedData.length === 0) {
    return typeof emptyMessage === 'string' ? (
      <Typography my={3} variant='h4' align='center'>
        {emptyMessage}
      </Typography>
    ) : (
      <>{emptyMessage}</>
    )
  }

  const hasStickyCells = columns.some((col) => col.sticky)

  const columnsToRender = columns.filter((col) => !col.skipRender)

  const tableContent = (
    <Table
      size={tableSize}
      sx={[
        hasStickyCells && {
          borderCollapse: 'separate',
          [`& .${tableCellClasses.root}:last-of-type`]: (theme) => ({
            position: 'sticky',
            right: 0,
            zIndex: 3,
            backgroundColor: LIGHT_CELL_BACKGROUND,
            ...theme.applyStyles('dark', { backgroundColor: stickyDarkCellBackgroundColor })
          })
        },
        removeLastBorderBottom && { '& tbody tr:last-child td': { borderBottom: 'none' } }
      ]}
    >
      <TableHead>
        <TableRow>
          {columnsToRender.map((column) => (
            <TableCell
              key={column.key}
              align={column.align}
              sx={{ minWidth: column.minWidth, maxWidth: column.maxWidth }}
            >
              {column.sortable ? (
                <TableSortLabel
                  active={isSortActive(column)}
                  direction={getSortDirection(column)}
                  onClick={handleSortClick(column)}
                >
                  {column.label}
                </TableSortLabel>
              ) : (
                column.label
              )}
            </TableCell>
          ))}
        </TableRow>
        <TableRow />
      </TableHead>
      <TableBody>
        {sortedData.map((item) => {
          const itemId = String(item[idField as string])
          const isItemFavorite = isFavorite(item)

          return (
            <TableRow
              key={itemId}
              sx={[selectedRowId === itemId && { backgroundColor: 'divider' }]}
            >
              {columnsToRender.map((column, index) => (
                <TableCell
                  key={column.key}
                  align={column.align}
                  sx={{
                    minWidth: column.minWidth,
                    maxWidth: column.maxWidth,
                    // Special styling for first cell with favorites
                    ...(index === 0 &&
                      favorites?.enabled && {
                        pl: 0,
                        [`&:hover .${FAVOURITE_BUTTON_CLASS_NAME}`]: { opacity: 1 },
                        ...(isItemFavorite && {
                          [`& .${FAVOURITE_BUTTON_CLASS_NAME}`]: { opacity: 1 }
                        })
                      })
                  }}
                >
                  {index === 0 && favorites?.enabled ? (
                    <Stack direction='row' alignItems='center' useFlexGap gap={0.5}>
                      {renderFavoriteButton(item)}
                      {column.render(item)}
                    </Stack>
                  ) : (
                    column.render(item)
                  )}
                </TableCell>
              ))}
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )

  if (enableOverflowScroll) {
    return <Box overflow='scroll'>{tableContent}</Box>
  }

  return tableContent
}
