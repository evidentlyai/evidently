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
import { api } from 'api/RemoteApi'
import { TextWithCopyIcon } from 'Components/TextWithCopyIcon'
import { formatDate } from 'Utils/Datetime'
import { DownloadButton } from 'Components/DownloadButton'
import { crumbFunction } from 'Components/BreadCrumbs'

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

  const showTestSuiteByIdMatch = matches.find(({ id }) => id === 'show-test-suite-by-id')

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
