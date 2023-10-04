import {
  Box,
  Button,
  Chip,
  Grid,
  Link,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField
} from '@material-ui/core'
import {
  Link as RouterLink,
  LoaderFunctionArgs,
  useLoaderData,
  useParams,
  useMatches,
  Outlet,
  useSearchParams
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { TextWithCopyIcon } from 'Components/TextWithCopyIcon'
import { formatDate } from 'Utils/Datetime'
import { DownloadButton } from 'Components/DownloadButton'
import { crumbFunction } from 'Components/BreadCrumbs'
import { useUpdateQueryStringValueWithoutNavigation } from 'hooks/useUpdateQueryStringValueWithoutNavigation'
import { useState } from 'react'
import { Autocomplete } from '@material-ui/lab'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getTestSuites(params.projectId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname, params }) => ({ to: pathname, linkText: 'Test Suites' })
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
      <Box sx={{ padding: 20 }}>
        <Grid container>
          <Grid item xs={5}>
            <Autocomplete
              multiple
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
              {filteredTestSuites.map((testSuite, idx) => (
                <TableRow key={`ts-${idx}`}>
                  <TableCell>
                    <TextWithCopyIcon showText={testSuite.id} copyText={testSuite.id} />
                  </TableCell>

                  <TableCell>
                    <Box maxWidth={250} display={'flex'} alignContent={'center'} flexWrap={'wrap'}>
                      {testSuite.tags.map((tag, index) => (
                        <Chip style={{ margin: '3px' }} key={index} label={tag} />
                      ))}
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
