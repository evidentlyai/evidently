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
  useMatches,
  Outlet
} from 'react-router-dom'
import invariant from 'tiny-invariant'
import { api } from '../../api/RemoteApi'
import { TextWithCopyIcon } from '../TextWithCopyIcon'
import { formatDate } from '../../Utils/Datetime'
import { DownloadButton } from '../DownloadButton'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  return api.getTestSuites(params.projectId)
}

export const TestSuitesList = () => {
  const { projectId } = useParams()
  const testSuites = useLoaderData() as Awaited<ReturnType<typeof loader>>
  const matches = useMatches()

  const showTestSuiteByIdMatch = matches.find(({ id }) => id === 'show-test-suite-by-id')

  if (showTestSuiteByIdMatch) {
    return (
      <Grid container>
        <Grid item xs={12}>
          {/* {showTestSuiteByIdMatch.params.reportId && (
            <TextWithCopyIcon
              showText={showTestSuiteByIdMatch.params.reportId}
              copyText={showTestSuiteByIdMatch.params.reportId}
            />
          )} */}
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
                <TableCell>Test Suite ID</TableCell>
                <TableCell>Timestamp</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {testSuites.map((testSuite, idx) => (
                <TableRow key={`ts-${idx}`}>
                  <TableCell>
                    <TextWithCopyIcon showText={testSuite.id} copyText={testSuite.id} />
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
