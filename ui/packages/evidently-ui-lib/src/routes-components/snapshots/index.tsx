import { useMemo, useState } from 'react'

import {
  Box,
  Button,
  FormControlLabel,
  Grid,
  Switch,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableSortLabel,
  TextField,
  Typography
} from '@mui/material'

import {
  Link as RouterLink,
  useLoaderData,
  useParams,
  Outlet,
  useMatches,
  useSearchParams,
  useSubmit,
  useNavigation,
  ShouldRevalidateFunction
} from 'react-router-dom'

import type { MetadataValueType } from '~/api'

import { useLocalStorage } from '@uidotdev/usehooks'

import JsonView from 'react18-json-view'
import 'react18-json-view/src/style.css'
import './override-react18-json-view.css'

import { TextWithCopyIcon } from '~/components/TextWithCopyIcon'
import { DownloadButton } from '~/components/DownloadButton'
import { HidedTags } from '~/components/HidedTags'
import { crumbFunction } from '~/components/BreadCrumbs'
import { Autocomplete } from '@mui/material'
import { useUpdateQueryStringValueWithoutNavigation } from '~/hooks/useUpdateQueryStringValueWithoutNavigation'
import dayjs from 'dayjs'
import { loaderData } from './data'

export const shouldRevalidate: ShouldRevalidateFunction = () => true

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({
    to: pathname,
    linkText: pathname.split('/').reverse()[0] === 'reports' ? 'Reports' : 'Test Suites'
  })
}

const metadataToOneString: (metadata: MetadataValueType) => string = (
  metadata: MetadataValueType
) =>
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

export const SnapshotTemplate = ({ type }: { type: 'report' | 'test suite' }) => {
  const { projectId } = useParams()
  const snapshots = useLoaderData() as loaderData
  const matches = useMatches()
  const submit = useSubmit()
  const navigation = useNavigation()
  const isNavigation = navigation.state !== 'idle'

  const [searchParams] = useSearchParams()
  const [sortByTimestamp, setSortByTimestamp] = useState<undefined | 'desc' | 'asc'>('desc')
  const [isCollapsedJson, setIsCollapsedJson] = useLocalStorage('show-full-json-metadata', false)
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])
  const [metadataQuery, setMetadataQuery] = useState(() => searchParams.get('metadata-query') || '')

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))
  useUpdateQueryStringValueWithoutNavigation('metadata-query', String(metadataQuery))

  // @ts-ignore
  const hideSnapshotsList = matches.find(({ handle }) => handle?.hide?.snapshotList === true)

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

  if (hideSnapshotsList) {
    return <Outlet />
  }

  return (
    <>
      <Box sx={{ padding: 2 }}>
        <Grid container gap={2} alignItems={'flex-end'}>
          <Grid item xs={12}>
            <Box display="flex" justifyContent="flex-end">
              <Button
                variant="outlined"
                onClick={() => submit(null, { method: 'post' })}
                color="primary"
                disabled={isNavigation}
              >
                refresh {`${type}s`}
              </Button>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Autocomplete
              multiple
              limitTags={2}
              value={selectedTags}
              onChange={(_, newSelectedTags) => setTags(newSelectedTags)}
              options={ALL_TAGS}
              renderInput={(params) => (
                <TextField {...params} variant="standard" label="Filter by Tags" />
              )}
            />
          </Grid>

          <Grid item xs={12} md={7}>
            <Box display={'flex'} alignItems={'flex-end'} gap={2}>
              <TextField
                fullWidth
                value={metadataQuery}
                onChange={(event) => setMetadataQuery(event.target.value)}
                variant="standard"
                label="Search in Metadata"
              />

              <Box minWidth={220} display={'flex'} justifyContent={'center'}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={isCollapsedJson}
                      onChange={(event) => setIsCollapsedJson(event.target.checked)}
                    ></Switch>
                  }
                  label="Hide Metadata"
                />
              </Box>
            </Box>
          </Grid>
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              {type === 'report'
                ? 'Report ID'
                : type === 'test suite'
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
            <TableCell>Actions</TableCell>
          </TableRow>
          <TableRow></TableRow>
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
                <JsonView
                  collapsed={isCollapsedJson}
                  src={snapshot.metadata}
                  theme="atom"
                  enableClipboard={false}
                />
              </TableCell>
              <TableCell>
                <Typography variant="body2">
                  {dayjs(snapshot.timestamp).locale('en-gb').format('llll')}
                </Typography>
              </TableCell>
              <TableCell>
                <Box display={'flex'} justifyContent={'center'} flexWrap={'wrap'} gap={1}>
                  <Button component={RouterLink} to={`${snapshot.id}`}>
                    View
                  </Button>
                  <DownloadButton
                    downloadLink={`/api/projects/${projectId}/${snapshot.id}/download`}
                  />
                </Box>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}
