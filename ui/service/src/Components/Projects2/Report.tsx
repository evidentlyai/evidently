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
import { DashboardContent } from '../../lib/components/DashboardContent'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')
  invariant(params.reportId, 'missing reportId')

  return api.getDashboard(params.projectId, params.reportId)
}

export const Report = () => {
  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>
  return <DashboardContent info={data} />
}
