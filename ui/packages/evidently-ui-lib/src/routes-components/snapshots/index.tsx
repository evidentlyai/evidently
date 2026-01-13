import { useEffect, useMemo, useState } from 'react'

import {
  Box,
  Button,
  type ButtonOwnProps,
  Checkbox,
  FormControlLabel,
  Grid,
  IconButton,
  Stack,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
  TextField,
  Tooltip,
  Typography
} from '@mui/material'

import { useLocalStorage } from '@uidotdev/usehooks'

import {
  Delete as DeleteIcon,
  FirstPage as FirstPageIcon,
  KeyboardArrowLeft,
  KeyboardArrowRight,
  LastPage as LastPageIcon
} from '@mui/icons-material'
import { Autocomplete } from '@mui/material'
import type { DownloadSnapshotURL, MetadataModel, ReportModel } from '~/api/types'
import { DownloadButton } from '~/components/Actions/DownloadButton'
import { HidedTags } from '~/components/Tags/HidedTags'
import { JsonViewThemed } from '~/components/Utils/JsonView'
import { TextWithCopyIcon } from '~/components/Utils/TextWithCopyIcon'
import { useUpdateQueryStringValueWithoutNavigation } from '~/hooks/useUpdateQueryStringValueWithoutNavigation'

import dayjs from 'dayjs'
import 'dayjs/locale/en-gb'
import localizedFormat from 'dayjs/plugin/localizedFormat'
dayjs.extend(localizedFormat)

const metadataToOneString: (metadata: MetadataModel) => string = (metadata: MetadataModel) =>
  Object.values(metadata)
    .map((value) => {
      if (Array.isArray(value)) {
        return value.join(' ')
      }

      if (typeof value === 'object') {
        return metadataToOneString(value)
      }

      return value
    })
    .join(' ')

const SnapshotNameAndID = (params: { name?: string | null; id: string }) => {
  return (
    <>
      {params.name ? (
        <Stack>
          <Typography>{params.name}</Typography>
          <Typography component={'div'} fontSize={'xx-small'}>
            <TextWithCopyIcon showText={params.id} copyText={params.id} tooltip={'Copy ID'} />
          </Typography>
        </Stack>
      ) : (
        <TextWithCopyIcon showText={params.id} copyText={params.id} tooltip={'Copy ID'} />
      )}
    </>
  )
}

type EmptyActionWrapperProps = {
  children: React.ReactNode
  snapshot: ReportModel
}

const EmptyActionWrapper = ({ children }: EmptyActionWrapperProps) => <>{children}</>

type SnapshotActionsWrapperProps = {
  query: Partial<Record<string, string>>
  projectId: string
  disabled?: boolean
  snapshots: ReportModel[]
  LinkToSnapshot: (props: { snapshotId: string; projectId: string }) => JSX.Element
  ActionsWrapper?: ({
    children,
    snapshot
  }: { children: React.ReactNode; snapshot: ReportModel }) => JSX.Element
  slots?: {
    additionalSnapshotActions?: (args: { snapshotId: string; projectId: string }) => JSX.Element
    donwloadButtonVariant?: ButtonOwnProps['variant']
  }
  onReloadSnapshots: () => void
  onDeleteSnapshot: ({ snapshotId }: { snapshotId: string }) => void
  downloadLink: DownloadSnapshotURL
  snapshotSelection?: { title: string; action: (snapshots: string[]) => void }
}

type TablePaginationActionsProps = {
  count: number
  page: number
  rowsPerPage: number
  onPageChange: (event: React.MouseEvent<HTMLButtonElement>, newPage: number) => void
}

function TablePaginationActions({
  count,
  page,
  rowsPerPage,
  onPageChange
}: TablePaginationActionsProps) {
  const handleFirstPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, 0)
  }

  const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, page - 1)
  }

  const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, page + 1)
  }

  const handleLastPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1))
  }

  const isLastPage = page >= Math.ceil(count / rowsPerPage) - 1

  return (
    <Box sx={{ flexShrink: 0, ml: 2.5 }}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label='first page'
      >
        <FirstPageIcon />
      </IconButton>
      <IconButton onClick={handleBackButtonClick} disabled={page === 0} aria-label='previous page'>
        <KeyboardArrowLeft />
      </IconButton>
      <IconButton onClick={handleNextButtonClick} disabled={isLastPage} aria-label='next page'>
        <KeyboardArrowRight />
      </IconButton>
      <IconButton onClick={handleLastPageButtonClick} disabled={isLastPage} aria-label='last page'>
        <LastPageIcon />
      </IconButton>
    </Box>
  )
}

export const SnapshotsListTemplate = (props: SnapshotActionsWrapperProps) => {
  const {
    query,
    slots,
    snapshots,
    disabled,
    projectId,
    LinkToSnapshot,
    onReloadSnapshots,
    onDeleteSnapshot,
    downloadLink,
    snapshotSelection,
    ActionsWrapper = EmptyActionWrapper
  } = props

  const [sortByTimestamp, setSortByTimestamp] = useState<undefined | 'desc' | 'asc'>('desc')
  const [isCollapsedJson, setIsCollapsedJson] = useLocalStorage('show-full-json-metadata', false)
  const [selectedTags, setTags] = useState(() => query.tags?.split(',') || [])
  const [metadataQuery, setMetadataQuery] = useState(() => query['metadata-query'] || '')

  // Pagination state
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))
  useUpdateQueryStringValueWithoutNavigation('metadata-query', String(metadataQuery))

  const ALL_TAGS = useMemo(
    () => Array.from(new Set(snapshots.flatMap(({ tags }) => tags))),
    [snapshots]
  )

  const filteredSnapshotsByTags = useMemo(
    () =>
      snapshots.filter(({ tags }) => selectedTags.every((candidate) => tags.includes(candidate))),
    [snapshots, selectedTags]
  )

  const filteredSnapshotsByMetadata = useMemo(
    () =>
      filteredSnapshotsByTags.filter(({ metadata }) => {
        if (metadataQuery === '') {
          return true
        }

        return metadataToOneString(metadata).includes(metadataQuery)
      }),
    [filteredSnapshotsByTags, metadataQuery]
  )

  const resultSnapshots = useMemo(
    () =>
      sortByTimestamp === undefined
        ? filteredSnapshotsByMetadata
        : filteredSnapshotsByMetadata.sort((a, b) => {
            const [first, second] = [Date.parse(a.timestamp), Date.parse(b.timestamp)]
            const diff = first - second
            if (sortByTimestamp === 'desc') {
              return -diff
            }

            if (sortByTimestamp === 'asc') {
              return diff
            }

            return 0
          }),
    [filteredSnapshotsByMetadata, sortByTimestamp]
  )

  // Reset to first page when filters change
  useEffect(() => {
    setPage(0)
  }, [selectedTags, metadataQuery, sortByTimestamp])

  // Paginate results
  const paginatedSnapshots = useMemo(
    () => resultSnapshots.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [resultSnapshots, page, rowsPerPage]
  )

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(Number.parseInt(event.target.value, 10))
    setPage(0)
  }

  const [selectedSnapshots, setSelectedSnapshots] = useState<Set<string>>(new Set())
  const isSnapshotSelected = (id: string) => selectedSnapshots.has(id)

  const FilterComponent = (
    <Box sx={{ padding: 2 }}>
      <Grid container gap={2} alignItems={'flex-end'} justifyContent={'space-between'}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Autocomplete
            multiple
            limitTags={2}
            value={selectedTags}
            onChange={(_, newSelectedTags) => setTags(newSelectedTags)}
            options={ALL_TAGS}
            renderInput={(params) => (
              <TextField {...params} variant='standard' label='Filter by Tags' />
            )}
          />
        </Grid>
        <Grid size={{ xs: 12, md: 7 }}>
          <Box display={'flex'} alignItems={'flex-end'} gap={2}>
            <TextField
              fullWidth
              value={metadataQuery}
              onChange={(event) => setMetadataQuery(event.target.value)}
              variant='standard'
              label='Search in Metadata'
            />
            <Box minWidth={220} display={'flex'} justifyContent={'center'}>
              <FormControlLabel
                control={
                  <Switch
                    checked={isCollapsedJson}
                    onChange={(event) => setIsCollapsedJson(event.target.checked)}
                  />
                }
                label='Hide Metadata'
              />
            </Box>
            <Box display='flex' justifyContent='flex-end'>
              <Button
                sx={{ minWidth: 160 }}
                variant='outlined'
                onClick={() => {
                  onReloadSnapshots()
                }}
                color='primary'
                disabled={disabled}
              >
                refresh reports
              </Button>
            </Box>
            {snapshotSelection && (
              <Box display='flex' justifyContent='flex-end'>
                <Button
                  sx={{ minWidth: 160 }}
                  variant='outlined'
                  onClick={() => {
                    snapshotSelection.action(Array.from(selectedSnapshots.values()))
                  }}
                  color='primary'
                  disabled={selectedSnapshots.size < 2}
                >
                  {snapshotSelection.title}
                </Button>
              </Box>
            )}
          </Box>
        </Grid>
      </Grid>
    </Box>
  )

  if (snapshots.length === 0) {
    return (
      <>
        {FilterComponent}
        <Typography my={3} variant='h4' align='center'>
          You don't have any reports yet.
        </Typography>
      </>
    )
  }

  return (
    <>
      {FilterComponent}
      <Table>
        <TableHead>
          <TableRow>
            {snapshotSelection && <TableCell />}
            <TableCell>Report ID</TableCell>
            <TableCell>Tags</TableCell>
            <TableCell>Metadata</TableCell>
            <TableCell>
              <TableSortLabel
                active={Boolean(sortByTimestamp)}
                direction={sortByTimestamp}
                onClick={() => {
                  setSortByTimestamp((prev) => {
                    if (prev === undefined) {
                      return 'desc'
                    }

                    if (prev === 'desc') {
                      return 'asc'
                    }

                    if (prev === 'asc') {
                      return undefined
                    }
                  })
                }}
              >
                Timestamp
              </TableSortLabel>
            </TableCell>
            <TableCell align='center'>Actions</TableCell>
          </TableRow>
          <TableRow />
        </TableHead>
        <TableBody>
          {paginatedSnapshots.map((snapshot) => (
            <TableRow key={`r-${snapshot.id}`}>
              {snapshotSelection && (
                <TableCell padding='checkbox'>
                  <Checkbox
                    color='primary'
                    checked={isSnapshotSelected(snapshot.id)}
                    onChange={() =>
                      setSelectedSnapshots((prev) => {
                        const newSet = new Set(prev)
                        prev.has(snapshot.id) ? newSet.delete(snapshot.id) : newSet.add(snapshot.id)
                        return newSet
                      })
                    }
                  />
                </TableCell>
              )}
              <TableCell>
                <SnapshotNameAndID id={snapshot.id} name={snapshot.name} />
              </TableCell>
              <TableCell>
                <Box maxWidth={250}>
                  <HidedTags
                    onClick={(clickedTag) => {
                      if (selectedTags.includes(clickedTag)) {
                        return
                      }

                      setTags([...selectedTags, clickedTag])
                    }}
                    tags={snapshot.tags}
                  />
                </Box>
              </TableCell>
              <TableCell>
                <JsonViewThemed
                  collapsed={isCollapsedJson}
                  value={snapshot.metadata}
                  enableClipboard={false}
                />
              </TableCell>
              <TableCell>
                <Typography variant='body2'>
                  {dayjs(snapshot.timestamp).locale('en-gb').format('llll')}
                </Typography>
              </TableCell>
              <TableCell>
                <Box display={'flex'} justifyContent={'center'} gap={1}>
                  <ActionsWrapper snapshot={snapshot}>
                    <>
                      <LinkToSnapshot snapshotId={snapshot.id} projectId={projectId} />

                      <DownloadButton
                        variant={slots?.donwloadButtonVariant || 'outlined'}
                        disabled={disabled ?? false}
                        downloadLink={
                          // normalize to string before replace (DownloadSnapshotURL isn't guaranteed to be string)
                          String(downloadLink)
                            .replace('{project_id}', projectId)
                            .replace('{snapshot_id}', snapshot.id)
                        }
                      />

                      {slots?.additionalSnapshotActions && (
                        <slots.additionalSnapshotActions
                          snapshotId={snapshot.id}
                          projectId={projectId}
                        />
                      )}

                      <Box>
                        <Tooltip title='delete snapshot' placement='top'>
                          <span>
                            <IconButton
                              onClick={() => {
                                onDeleteSnapshot({ snapshotId: snapshot.id })
                              }}
                              color='primary'
                              disabled={disabled}
                            >
                              <DeleteIcon />
                            </IconButton>
                          </span>
                        </Tooltip>
                      </Box>
                    </>
                  </ActionsWrapper>
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <TablePagination
        rowsPerPageOptions={[10, 30, 50]}
        component='div'
        count={resultSnapshots.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        ActionsComponent={TablePaginationActions}
      />
    </>
  )
}
