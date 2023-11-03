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
  LoaderFunctionArgs,
  useLoaderData,
  useParams,
  Outlet,
  useMatches,
  useSearchParams,
  ActionFunctionArgs,
  useSubmit
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from 'api/RemoteApi'
import { TextWithCopyIcon } from 'Components/TextWithCopyIcon'
import { formatDate } from 'Utils/Datetime'
import { DownloadButton } from 'Components/DownloadButton'
import { HidedTags } from 'Components/HidedTags'
import { crumbFunction } from 'Components/BreadCrumbs'
import { Autocomplete } from '@mui/material'
import { useUpdateQueryStringValueWithoutNavigation } from 'hooks/useUpdateQueryStringValueWithoutNavigation'

export const loader = async ({ params }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getReports(params.projectId)
}

export const action = async ({ params }: ActionFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.reloadProject(params.projectId)
}

type loaderData = Awaited<ReturnType<typeof loader>>

export const handle: { crumb: crumbFunction<loaderData> } = {
  crumb: (_, { pathname }) => ({ to: pathname, linkText: 'Reports' })
}

export const Component = () => {
  const { projectId } = useParams()

  const reports = useLoaderData() as loaderData
  const matches = useMatches()
  const submit = useSubmit()

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
      <Box sx={{ padding: 2 }}>
        <Grid container spacing={2} alignItems={'end'}>
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
          <Grid item flexGrow={2}>
            <Box display="flex" justifyContent="flex-end">
              <Button
                variant="outlined"
                onClick={() => submit(null, { method: 'post' })}
                color="primary"
              >
                Refresh Reports
              </Button>
            </Box>
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
                  <HidedTags
                    onClick={(clickedTag) => {
                      if (selectedTags.includes(clickedTag)) {
                        return
                      }

                      setTags([...selectedTags, clickedTag])
                    }}
                    tags={report.tags}
                  />
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
