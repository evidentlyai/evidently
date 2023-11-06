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
  TextField,
  Autocomplete
} from '@mui/material'

import {
  Link as RouterLink,
  useLoaderData,
  useParams,
  useMatches,
  Outlet,
  useSearchParams
} from 'react-router-dom'

import { TextWithCopyIcon } from '~/components/TextWithCopyIcon'
import { formatDate } from '~/utils'
import { DownloadButton } from '~/components/DownloadButton'
import { HidedTags } from '~/components/HidedTags'
import { crumbFunction } from '~/components/BreadCrumbs'
import { useUpdateQueryStringValueWithoutNavigation } from '~/hooks/useUpdateQueryStringValueWithoutNavigation'

import { loaderData } from './data'

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({ to: pathname, linkText: 'Test Suites' })
}

export const Component = () => {
  const { projectId } = useParams()
  const testSuites = useLoaderData() as loaderData
  const matches = useMatches()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  const showTestSuiteByIdMatch = matches.find(({ id }) => id === 'show-test-suite-by-id')

  const ALL_TAGS = showTestSuiteByIdMatch
    ? [] // skip calculation in this case
    : // calculate unique tags
      Array.from(new Set(testSuites.flatMap(({ tags }) => tags)))

  const filteredTestSuites = testSuites.filter(({ tags }) => {
    if (showTestSuiteByIdMatch) {
      return false
    }

    if (selectedTags.length === 0) {
      return true
    }

    return selectedTags.every((candidate) => tags.includes(candidate))
  })

  if (showTestSuiteByIdMatch) {
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
              id="tags"
              options={ALL_TAGS}
              renderInput={(params) => (
                <TextField {...params} variant="standard" label="Filter by Tags" />
              )}
            />
          </Grid>
          <Grid item xs={6} sm={6}></Grid>
        </Grid>
      </Box>
      <Grid container>
        <Grid item xs={12}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Test Suite ID</TableCell>
                <TableCell>Tags</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredTestSuites.map((testSuite) => (
                <TableRow key={`ts-${testSuite.id}`}>
                  <TableCell>
                    <TextWithCopyIcon showText={testSuite.id} copyText={testSuite.id} />
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
                        tags={testSuite.tags}
                      />
                    </Box>
                  </TableCell>

                  <TableCell>{formatDate(new Date(Date.parse(testSuite.timestamp)))}</TableCell>
                  <TableCell>
                    <Link component={RouterLink} to={`${testSuite.id}`}>
                      <Button>View</Button>
                    </Link>
                    <DownloadButton
                      downloadLink={`/api/projects/${projectId}/${testSuite.id}/download`}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Grid>
      </Grid>
    </>
  )
}
