import {
  Button,
  Grid,
  Link,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from '@material-ui/core'
import {
  Link as RouterLink,
  LoaderFunctionArgs,
  useLoaderData,
  useParams,
  Outlet,
  useMatch,
  useMatches
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from '../../api/RemoteApi'
import { TextWithCopyIcon } from '../TextWithCopyIcon'
import { formatDate } from '../../Utils/Datetime'
import { DownloadButton } from '../DownloadButton'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getReports(params.projectId)
}

export const ReportsList = () => {
  const { projectId } = useParams()
  const reports = useLoaderData() as Awaited<ReturnType<typeof loader>>
  const matches = useMatches()

  const showReportByIdMatch = matches.find(({ id }) => id === 'show-report-by-id')

  if (showReportByIdMatch) {
    return (
      <Grid container>
        <Grid item xs={12}>
          {showReportByIdMatch.params.reportId && (
            <TextWithCopyIcon
              showText={showReportByIdMatch.params.reportId}
              copyText={showReportByIdMatch.params.reportId}
            />
          )}
          {/* render it here in nested route */}
          <Outlet />
        </Grid>
      </Grid>
    )
  }

  return (
    <>
      <Grid container>
        <Grid item xs={12}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Report ID</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reports.map((report) => (
                <TableRow id={report.id}>
                  <TableCell>
                    <TextWithCopyIcon showText={report.id} copyText={report.id} />
                  </TableCell>
                  <TableCell>{formatDate(new Date(Date.parse(report.timestamp)))}</TableCell>
                  <TableCell>
                    <Link component={RouterLink} to={`${report.id}`}>
                      <Button>View</Button>
                    </Link>
                    <DownloadButton
                      downloadLink={`/api/projects/${projectId}/${report.id}/download`}
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
