import { Alert, AlertTitle, Box, Collapse, Grid, Typography } from '@mui/material'
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

  return api.getProjectDashboard(params.projectId, date_from, date_to, request.signal)
}

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const [searchParams, setSearchParams] = useSearchParams()

  const getOnChangeDate =
    (dateType: 'date_from' | 'date_to') => (dateValue: '' | null | dayjs.Dayjs) => {
      setSearchParams((params) => {
        params.delete(dateType)

        if (dateValue && dateValue.isValid()) {
          params.append(dateType, formatDate(new Date(dateValue.toISOString())))
        }

        return params
      })
    }

  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }

  const date_from = dayjs(searchParams.get('date_from') || dataRanges.minDate)
  const date_to = dayjs(searchParams.get('date_to') || dataRanges.maxDate)

  const isCorrectTimeInterval = date_from.isBefore(date_to)
  const isIncorrectTimeIntervalMessage = !isCorrectTimeInterval ? 'incorrect time interval' : ''

  return (
    <>
      <Grid
        container
        padding={1}
        zIndex={1}
        my={3}
        gap={2}
        justifyContent="flex-end"
        justifyItems={'center'}
      >
        <Grid item>
          <DateTimePicker
            {...dataRanges}
            slotProps={{
              textField: {
                variant: 'standard'
              }
            }}
            label="From"
            value={date_from}
            onChange={getOnChangeDate('date_from')}
          />
        </Grid>
        <Grid item>
          <Box height={1} display={'flex'} alignItems={'center'}>
            <Typography> – </Typography>
          </Box>
        </Grid>
        <Grid item>
          <DateTimePicker
            {...dataRanges}
            slotProps={{
              textField: {
                variant: 'standard'
              }
            }}
            label="To"
            value={date_to}
            onChange={getOnChangeDate('date_to')}
          />
        </Grid>
        <Grid item xs={12}>
          <Collapse unmountOnExit in={!isCorrectTimeInterval}>
            <Alert severity="error">
              <AlertTitle>Error</AlertTitle>
              {isIncorrectTimeIntervalMessage}
            </Alert>
          </Collapse>
        </Grid>
      </Grid>

      <Grid container spacing={3} direction="row" alignItems="stretch">
        {isCorrectTimeInterval && <DashboardContent info={data} />}
      </Grid>
    </>
  )
}
