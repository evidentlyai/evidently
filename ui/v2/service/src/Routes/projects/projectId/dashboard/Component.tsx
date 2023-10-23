import { Alert, AlertTitle, Box, Collapse, Grid, Typography } from '@mui/material'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'
import dayjs from 'dayjs'
import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router-dom'
import { DashboardContent } from 'evidently-ui/components/DashboardContent'
import { api } from 'api/RemoteApi'
import invariant from 'tiny-invariant'
import { useSearchParams } from 'react-router-dom'
import { formatDate } from 'Utils/Datetime'

type QueryAliases = 'FROM' | 'TO'
type QueryLiterals = 'date_from' | 'date_to'

const queryParams: Record<QueryAliases, QueryLiterals> = {
  FROM: 'date_from',
  TO: 'date_to'
}

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  const { searchParams } = new URL(request.url)

  let date_from = searchParams.get(queryParams.FROM)
  let date_to = searchParams.get(queryParams.TO)

  if (date_from && !dayjs(date_from).isValid()) {
    date_from = null
  }

  if (date_to && !dayjs(date_to).isValid()) {
    date_to = null
  }

  return api.getProjectDashboard(params.projectId, date_from, date_to, request.signal)
}

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const [searchParams, setSearchParams] = useSearchParams()

  const getOnChangeDate = (dateType: QueryLiterals) => (dateValue: dayjs.Dayjs | null) => {
    setSearchParams((params) => {
      params.delete(dateType)

      if (dateValue) {
        params.append(dateType, formatDate(dateValue.toDate()))
      }

      return params
    })
  }

  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }

  const date_from = dayjs(searchParams.get(queryParams.FROM) || dataRanges.minDate)
  const date_to = dayjs(searchParams.get(queryParams.TO) || dataRanges.maxDate)

  const isCorrectTimeInterval =
    date_from.isValid() && date_to.isValid() && date_from.isBefore(date_to)

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
            minDate={dataRanges.minDate}
            maxDate={dataRanges.maxDate && date_to}
            slotProps={{
              textField: {
                variant: 'standard'
              }
            }}
            label="From"
            value={date_from}
            onChange={getOnChangeDate(queryParams.FROM)}
          />
        </Grid>
        <Grid item>
          <Box height={1} display={'flex'} alignItems={'center'}>
            <Typography> – </Typography>
          </Box>
        </Grid>
        <Grid item>
          <DateTimePicker
            minDate={dataRanges.minDate && date_from}
            maxDate={dataRanges.maxDate}
            slotProps={{
              textField: {
                variant: 'standard'
              }
            }}
            label="To"
            value={date_to}
            onChange={getOnChangeDate(queryParams.TO)}
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
