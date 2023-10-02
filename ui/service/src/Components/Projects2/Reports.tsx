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
  useMatches,
  RouteObject
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from '../../api/RemoteApi'
import { TextWithCopyIcon } from '../TextWithCopyIcon'
import { formatDate } from '../../Utils/Datetime'
import { DownloadButton } from '../DownloadButton'
import { satisfies } from 'semver'
import { crumbFunction } from '../BreadCrumbs'

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

  const showReportByIdMatch = matches.find(({ id }) => id === 'show-report-by-id')

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

export default {
  id: 'reports',
  path: 'reports',
  loader,
  Component,
  handle
} satisfies RouteObject
