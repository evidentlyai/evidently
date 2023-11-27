import { useState } from 'react'

import {
  Box,
  Button,
  Grid,
  Link,
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
  useSearchParams
} from 'react-router-dom'

import { TextWithCopyIcon } from '~/components/TextWithCopyIcon'
import { DownloadButton } from '~/components/DownloadButton'
import { HidedTags } from '~/components/HidedTags'
import { crumbFunction } from '~/components/BreadCrumbs'
import { Autocomplete } from '@mui/material'
import { useUpdateQueryStringValueWithoutNavigation } from '~/hooks/useUpdateQueryStringValueWithoutNavigation'
import { loaderData } from './data'
import dayjs from 'dayjs'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({
    to: pathname,
    linkText: pathname.split('/').reverse()[0] === 'reports' ? 'Reports' : 'Test Suites'
  })
}

export const SnapshotTemplate = ({ type }: { type: 'report' | 'test-suite' }) => {
  const { projectId } = useParams()
  const snapshots = useLoaderData() as loaderData
  const matches = useMatches()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])
  const [sortByTimestamp, setSortByTimestamp] = useState<undefined | 'desc' | 'asc'>('desc')

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  // @ts-ignore
  const hideSnapshotsList = matches.find(({ handle }) => handle?.hide?.snapshotList === true)

  if (hideSnapshotsList) {
    return (
      <Grid container>
        <Grid item xs={12}>
          <Outlet />
        </Grid>
      </Grid>
    )
  }

  const ALL_TAGS = Array.from(new Set(snapshots.flatMap(({ tags }) => tags)))

  const filteredSnapshots = snapshots.filter(({ tags }) =>
    selectedTags.every((candidate) => tags.includes(candidate))
  )

  const sortedByTimestamp =
    sortByTimestamp === undefined
      ? filteredSnapshots
      : filteredSnapshots.sort((a, b) => {
          const [first, second] = [Date.parse(a.timestamp), Date.parse(b.timestamp)]
          const diff = first - second
          if (sortByTimestamp === 'desc') {
            return -diff
          }

          if (sortByTimestamp === 'asc') {
            return diff
          }

          return 0
        })

  return (
    <>
      <Box sx={{ padding: 2 }}>
        <Grid container>
          <Grid item xs={12} md={6}>
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
        </Grid>
      </Box>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>
              {type === 'report'
                ? 'Report ID'
                : type === 'test-suite'
                ? 'Test Suite ID'
                : 'indefined'}
            </TableCell>
            <TableCell>Tags</TableCell>
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
          {sortedByTimestamp.map((snapshot) => (
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
                <Typography variant="body2">
                  {dayjs(snapshot.timestamp).locale('en-gb').format('llll')}
                </Typography>
              </TableCell>
              <TableCell>
                <Link component={RouterLink} to={`${snapshot.id}`}>
                  <Button>View</Button>
                </Link>
                <DownloadButton
                  downloadLink={`/api/projects/${projectId}/${snapshot.id}/download`}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}
