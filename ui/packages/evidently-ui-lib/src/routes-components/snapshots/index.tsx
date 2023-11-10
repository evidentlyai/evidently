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
  TextField
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
import { formatDate } from '~/utils'
import { DownloadButton } from '~/components/DownloadButton'
import { HidedTags } from '~/components/HidedTags'
import { crumbFunction } from '~/components/BreadCrumbs'
import { Autocomplete } from '@mui/material'
import { useUpdateQueryStringValueWithoutNavigation } from '~/hooks/useUpdateQueryStringValueWithoutNavigation'
import { loaderData } from './data'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({ to: pathname, linkText: 'Reports' })
}

export const SnapshotTemplate = ({ type }: { type: 'report' | 'test-suite' }) => {
  const { projectId } = useParams()
  const snapshots = useLoaderData() as loaderData
  const matches = useMatches()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  const showSnapshotByIdMatch = matches.find(({ id }) => id === `show-${type}-by-id`)

  const ALL_TAGS = showSnapshotByIdMatch
    ? [] // skip calculation in this case
    : // calculate unique tags
      Array.from(new Set(snapshots.flatMap(({ tags }) => tags)))

  const filteredSnapshots = snapshots.filter(({ tags }) => {
    if (showSnapshotByIdMatch) {
      return false
    }

    if (selectedTags.length === 0) {
      return true
    }

    return selectedTags.every((candidate) => tags.includes(candidate))
  })

  if (showSnapshotByIdMatch) {
    return (
      <Grid container>
        <Grid item xs={12}>
          <Outlet />
        </Grid>
      </Grid>
    )
  }

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
            <TableCell>Timestamp</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
          <TableRow></TableRow>
        </TableHead>
        <TableBody>
          {filteredSnapshots.map((snapshot) => (
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
              <TableCell>{formatDate(new Date(Date.parse(snapshot.timestamp)))}</TableCell>
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
