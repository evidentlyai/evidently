import { useState } from 'react'
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
  Outlet,
  useMatches,
  useSearchParams
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { TextWithCopyIcon } from 'Components/TextWithCopyIcon'
import { formatDate } from 'Utils/Datetime'
import { DownloadButton } from 'Components/DownloadButton'
import { HidedTags } from 'Components/HidedTags'
import { crumbFunction } from 'Components/BreadCrumbs'
import { Autocomplete } from '@material-ui/lab'
import { useUpdateQueryStringValueWithoutNavigation } from 'hooks/useUpdateQueryStringValueWithoutNavigation'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getReports(params.projectId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (data, { pathname, params }) => ({ to: pathname, linkText: 'Reports' })
}

export const Component = () => {
  const { projectId } = useParams()
  const reports = useLoaderData() as loaderData
  const matches = useMatches()

  const [searchParams] = useSearchParams()
  const [selectedTags, setTags] = useState(() => searchParams.get('tags')?.split(',') || [])

  useUpdateQueryStringValueWithoutNavigation('tags', selectedTags.join(','))

  const showReportByIdMatch = matches.find(({ id }) => id === 'show-report-by-id')

  const ALL_TAGS = showReportByIdMatch
    ? [] // skip calculation in this case
    : // calculate unique tags
      Array.from(new Set(reports.flatMap(({ tags }) => tags)))

  const filteredReports = reports.filter(({ tags }) => {
    if (showReportByIdMatch) {
      return false
    }

    if (selectedTags.length === 0) {
      return true
    }

    return selectedTags.every((candidate) => tags.includes(candidate))
  })

  if (showReportByIdMatch) {
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
            <TableCell>Report ID</TableCell>
            <TableCell>Tags</TableCell>
            <TableCell>Timestamp</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
          <TableRow></TableRow>
        </TableHead>
        <TableBody>
          {filteredReports.map((report) => (
            <TableRow key={`r-${report.id}`}>
              <TableCell>
                <TextWithCopyIcon showText={report.id} copyText={report.id} />
              </TableCell>
              <TableCell>
                <Box maxWidth={250}>
                  <HidedTags id={report.id} tags={report.tags} />
                </Box>
              </TableCell>
              <TableCell>{formatDate(new Date(Date.parse(report.timestamp)))}</TableCell>
              <TableCell>
                <Link component={RouterLink} to={`${report.id}`}>
                  <Button>View</Button>
                </Link>
                <DownloadButton downloadLink={`/api/projects/${projectId}/${report.id}/download`} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  )
}
