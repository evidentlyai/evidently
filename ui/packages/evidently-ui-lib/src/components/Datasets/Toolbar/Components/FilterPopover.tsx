import { FilterList as FilterListIcon } from '@mui/icons-material'
import { CloseRounded as CloseRoundedIcon } from '@mui/icons-material'
import {
  Autocomplete,
  Box,
  Button,
  Chip,
  Divider,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Popover,
  Select,
  Stack,
  TextField,
  Tooltip,
  Typography
} from '@mui/material'
import type { GridColDef } from '@mui/x-data-grid'
import PopupState, { bindPopover, bindTrigger } from 'material-ui-popup-state'
import { useState } from 'react'
import type { DatasetFilter } from '~/api/types'
import type { Expect, TYPE_SATISFIED } from '~/api/types/utils'
import { Counter } from '~/components/Utils/Counter'

type NumericDatasetFilter = Extract<DatasetFilter, { value: number }>
type NumericType = Exclude<NumericDatasetFilter['type'], null | undefined>

type StringDatasetFilter = Extract<DatasetFilter, { value: string }>
type StringType = Exclude<StringDatasetFilter['type'], null | undefined>

const VALUE_TYPE_TO_OPERATORS = {
  string: ['contains', 'ends_with', 'starts_with'],
  number: ['eq', 'not_eq', 'gt', 'gte', 'lt', 'lte']
} as const

export type __TESTS_PASSED = Expect<
  | TYPE_SATISFIED<NumericType, (typeof VALUE_TYPE_TO_OPERATORS.number)[number]>
  | TYPE_SATISFIED<StringType, (typeof VALUE_TYPE_TO_OPERATORS.string)[number]>
>

const OPERATOR_TO_DISPLAY_NAME: Record<Exclude<DatasetFilter['type'], null | undefined>, string> = {
  contains: 'contains',
  ends_with: 'ends with',
  starts_with: 'starts with',
  eq: '=',
  gt: '>',
  gte: '≥',
  lt: '<',
  lte: '≤',
  not_eq: '≠'
}

type FilterCompoentProps = {
  filters: DatasetFilter[]
  setFilters: (filters: DatasetFilter[]) => void
  columns: GridColDef[]
}

export const FilterCompoent = (props: FilterCompoentProps) => {
  const { filters, setFilters, columns } = props

  const [column, setColumn] = useState<GridColDef | null>(null)
  const [newFilterDef, setNewFilter] = useState<DatasetFilter | null>(null)

  return (
    <PopupState variant='popover'>
      {(popupState) => (
        <Box>
          <Box position={'relative'}>
            <Button size='small' startIcon={<FilterListIcon />} {...bindTrigger(popupState)}>
              Filters
            </Button>
            <Counter
              count={filters.length}
              sx={{ position: 'absolute', top: 1, right: -8, minWidth: '15px', height: '15px' }}
            />
          </Box>
          <Popover
            {...bindPopover(popupState)}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
            transformOrigin={{ vertical: 'top', horizontal: 'left' }}
          >
            <Box p={2}>
              {filters.length === 0 && <Typography>You don't have any filters yet</Typography>}

              <Stack direction={'row'} alignItems={'center'} flexWrap={'wrap'} maxWidth={'sm'}>
                {filters.map((f, index) => (
                  // biome-ignore lint/correctness/useJsxKeyInIterable: fine
                  <Stack direction={'row'} alignItems={'center'}>
                    <Stack
                      direction={'row'}
                      position={'relative'}
                      py={1}
                      pr={3}
                      alignItems={'center'}
                      gap={1}
                    >
                      {index > 0 && <Typography>and</Typography>}

                      <Chip
                        label={`"${f.column}" ${f.type ? OPERATOR_TO_DISPLAY_NAME[f.type] : ''} ${typeof f.value === 'string' ? `"${f.value}"` : f.value}`}
                      />

                      <Tooltip title='Delete filter' placement='top'>
                        <IconButton
                          sx={{ position: 'absolute', top: 0, right: 0 }}
                          size={'small'}
                          aria-label='delete'
                          onClick={() =>
                            setFilters(filters.filter((_, fIndex) => fIndex !== index))
                          }
                        >
                          <CloseRoundedIcon sx={{ fontSize: 17 }} />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                  </Stack>
                ))}
              </Stack>

              <Divider sx={{ my: 2 }} />
              <Stack direction={'row'} gap={2} alignItems={'center'}>
                <Box minWidth={(column?.headerName ?? '').length * 5 + 150}>
                  <Autocomplete
                    value={column}
                    onChange={(_, value) => {
                      setColumn(value)

                      if (!value) {
                        setNewFilter(null)
                        return
                      }

                      setNewFilter(columnToFilterDef(value))
                    }}
                    size='small'
                    getOptionLabel={(e) => e.headerName ?? ''}
                    getOptionKey={(e) => e.field}
                    ListboxProps={{ sx: { maxHeight: 350 } }}
                    options={columns}
                    renderInput={(params) => <TextField {...params} label='Column' />}
                  />
                </Box>

                {column?.type && (column.type === 'number' || column.type === 'string') ? (
                  <>
                    <Box minWidth={150}>
                      <FormControl size='small' fullWidth>
                        <InputLabel>Operator</InputLabel>
                        <Select
                          size='small'
                          label='Operator'
                          value={newFilterDef?.type ?? ''}
                          onChange={(e) =>
                            setNewFilter((p) => {
                              return column.type === 'number'
                                ? {
                                    ...(p as NumericDatasetFilter),
                                    type: e.target.value as NumericType
                                  }
                                : column.type === 'string'
                                  ? {
                                      ...(p as StringDatasetFilter),
                                      type: e.target.value as StringType
                                    }
                                  : null
                            })
                          }
                        >
                          {VALUE_TYPE_TO_OPERATORS[column.type].map((operator) => (
                            <MenuItem value={operator} key={operator}>
                              {OPERATOR_TO_DISPLAY_NAME[operator]}
                            </MenuItem>
                          ))}
                        </Select>
                      </FormControl>
                    </Box>
                    <Box>
                      <TextField
                        label={'Value'}
                        type={column.type === 'number' ? 'number' : 'text'}
                        size='small'
                        value={newFilterDef?.value ?? ''}
                        onChange={(e) =>
                          setNewFilter((p) =>
                            column.type === 'string'
                              ? {
                                  ...(p as StringDatasetFilter),
                                  value: e.target.value
                                }
                              : column.type === 'number'
                                ? {
                                    ...(p as NumericDatasetFilter),
                                    value: (e.target.value === ''
                                      ? ''
                                      : Number(e.target.value)) as number
                                  }
                                : null
                          )
                        }
                      />
                    </Box>
                  </>
                ) : (
                  column?.type && (
                    <Box maxWidth={150}>
                      <Typography fontStyle={'italic'}>Unsupported for filtering</Typography>
                    </Box>
                  )
                )}

                <Button
                  variant='outlined'
                  disabled={
                    !newFilterDef ||
                    !newFilterDef.column ||
                    !newFilterDef.type ||
                    String(newFilterDef.value).length === 0
                  }
                  onClick={() => {
                    if (newFilterDef) {
                      setFilters([...filters, newFilterDef])
                    }
                  }}
                >
                  Add
                </Button>
              </Stack>
            </Box>
          </Popover>
        </Box>
      )}
    </PopupState>
  )
}

const columnToFilterDef: (column: GridColDef) => DatasetFilter | null = (column) => {
  const headerName = column.field ?? ''

  if (column.type === 'number') {
    return {
      type: VALUE_TYPE_TO_OPERATORS.number[0],
      column: headerName,
      value: 0
    } satisfies NumericDatasetFilter
  }

  if (column.type === 'string') {
    return {
      type: VALUE_TYPE_TO_OPERATORS.string[0],
      column: headerName,
      value: ''
    } satisfies StringDatasetFilter
  }

  return null
}
