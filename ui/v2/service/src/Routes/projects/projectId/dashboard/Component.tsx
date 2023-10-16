import { Box, Grid, Typography } from '@mui/material'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'
import dayjs from 'dayjs'
import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router-dom'
import { DashboardContent } from 'evidently-ui/components/DashboardContent'
import { api } from 'api/RemoteApi'
import invariant from 'tiny-invariant'
import { useSearchParams } from 'react-router-dom'
import { formatDate } from 'Utils/Datetime'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  const { searchParams } = new URL(request.url)
  const { date_from, date_to } = Object.fromEntries(searchParams.entries())

  invariant(params.projectId, 'missing projectId')

  return api.getProjectDashboard(params.projectId, date_from, date_to)
}

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')
  const [searchParams, setSearchParams] = useSearchParams()
  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>

  const date_from = searchParams.get('date_from')
  const date_to = searchParams.get('date_to')

  const getOnChangeDate =
    (dateType: 'date_from' | 'date_to') => (dateValue: '' | null | dayjs.Dayjs) => {
      setSearchParams((params) => {
        params.delete(dateType)

        if (dateValue) {
          params.append(dateType, formatDate(new Date(dateValue.toISOString())))
        }

        return params
      })
    }

  return (
    <>
      <Grid container my={3} gap={2} justifyContent="flex-end" justifyItems={'center'}>
        <Grid item>
          <Box display="flex" alignItems="center" height={1}>
            <Typography variant="h6">Date</Typography>
          </Box>
        </Grid>

        <Grid item>
          <DateTimePicker
            label="From"
            value={date_from && dayjs(date_from)}
            onChange={getOnChangeDate('date_from')}
          />
        </Grid>
        <Grid item>
          <DateTimePicker
            label="To"
            value={date_to && dayjs(date_to)}
            onChange={getOnChangeDate('date_to')}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} direction="row" alignItems="stretch">
        <DashboardContent info={data} />
      </Grid>
    </>
  )
}
