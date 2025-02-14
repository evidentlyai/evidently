import { useMemo, useState } from 'react'

import {
  Box,
  Button,
  type ButtonOwnProps,
  FormControlLabel,
  Grid,
  IconButton,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableSortLabel,
  TextField,
  Tooltip,
  Typography
} from '@mui/material'

import { useLocalStorage } from '@uidotdev/usehooks'

import { Delete as DeleteIcon } from '@mui/icons-material'
import { Autocomplete } from '@mui/material'
import type { DownloadSnapshotURL, MetadataModel, ReportModel, TestSuiteModel } from '~/api/types'
import { DownloadButton } from '~/components/DownloadButton'
import { HidedTags } from '~/components/HidedTags'
import { JsonViewThemed } from '~/components/JsonView'
import { TextWithCopyIcon } from '~/components/TextWithCopyIcon'
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

export const SnapshotsListTemplate = ({
  query,
  type,
  slots,
  snapshots,
  disabled,
  projectId,
  LinkToSnapshot,
  onReloadSnapshots,
  onDeleteSnapshot,
  ActionsWrapper = ({ children }) => <>{children}</>
}: {
  query: Partial<Record<string, string>>
  projectId: string
  disabled?: boolean
  snapshots: ReportModel[] | TestSuiteModel[]
  type: 'reports' | 'test suites'
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
}) => {
  const [sortByTimestamp, setSortByTimestamp] = useState<undefined | 'desc' | 'asc'>('desc')
  const [isCollapsedJson, setIsCollapsedJson] = useLocalStorage('show-full-json-metadata', false)
  const [selectedTags, setTags] = useState(() => query.tags?.split(',') || [])
  const [metadataQuery, setMetadataQuery] = useState(() => query['metadata-query'] || '')

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

  const FilterComponent = (
    <Box sx={{ padding: 2 }}>
      <Grid container gap={2} alignItems={'flex-end'} justifyContent={'space-around'}>
        <Grid item xs={12} md={4}>
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
        <Grid item xs={12} md={7}>
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
                refresh {type}
              </Button>
            </Box>
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
          You don't have any {type} yet.
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
            <TableCell>
              {type === 'reports'
                ? 'Report ID'
                : type === 'test suites'
                  ? 'Test Suite ID'
                  : 'indefined'}
            </TableCell>
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
          {resultSnapshots.map((snapshot) => (
            <TableRow key={`r-${snapshot.id}`}>
              <TableCell>
                <TextWithCopyIcon showText={snapshot.id} copyText={snapshot.id} />
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
                          // better type safety
                          (
                            '/api/projects/{project_id}/{snapshot_id}/download' satisfies DownloadSnapshotURL
                          )
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
                          <IconButton
                            onClick={() => {
                              if (confirm('Are you sure?') === true) {
                                onDeleteSnapshot({ snapshotId: snapshot.id })
                              }
                            }}
                            color='primary'
                            disabled={disabled}
                          >
                            <DeleteIcon />
                          </IconButton>
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
    </>
  )
}
