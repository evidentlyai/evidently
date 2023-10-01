import { Grid, TextField, Typography } from '@material-ui/core'
import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router'
import { DashboardContent } from '../../lib/components/DashboardContent'
import { api } from '../../api/RemoteApi'
import invariant from 'tiny-invariant'
import { useSearchParams } from 'react-router-dom'
import { formatDate } from '../../Utils/Datetime'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  const { searchParams } = new URL(request.url)
  const { date_from, date_to } = Object.fromEntries(searchParams.entries())

  invariant(params.projectId, 'missing projectId')

  return api.getProjectDashboard(params.projectId, date_from, date_to)
}

export const Dashboard = () => {
  const { projectId } = useParams()
  const [searchParams, setSearchParams] = useSearchParams()
  const { date_from, date_to } = Object.fromEntries(searchParams.entries())

  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>

  invariant(projectId, 'missing projectId')

  return (
    <>
      <Grid container justifyContent={'flex-end'}>
        <Grid item>
          <TextField
            id="from-datetime"
            label="From"
            type="datetime-local"
            defaultValue={date_from && formatDate(new Date(Date.parse(date_from)))}
            onChange={(event) => {
              let { value } = event.target
              console.log('value', value)
              setSearchParams(
                { ...Object.fromEntries(searchParams.entries()), date_from: value },
                { preventScrollReset: true, replace: true }
              )
            }}
            InputLabelProps={{
              shrink: true
            }}
            style={{ paddingRight: '20px' }}
          />
          <TextField
            id="to-datetime"
            label="To"
            type="datetime-local"
            defaultValue={date_to && formatDate(new Date(Date.parse(date_to)))}
            onChange={(event) => {
              let { value } = event.target
              console.log('value', value)
              setSearchParams(
                { ...Object.fromEntries(searchParams.entries()), date_to: value },
                { preventScrollReset: true, replace: true }
              )
            }}
            InputLabelProps={{
              shrink: true
            }}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} direction="row" alignItems="stretch">
        <DashboardContent info={data} />
      </Grid>
    </>
  )
}
