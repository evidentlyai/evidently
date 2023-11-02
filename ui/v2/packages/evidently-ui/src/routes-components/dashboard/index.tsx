import { Alert, AlertTitle, Box, Collapse, Grid, Typography } from '@mui/material'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'
import { useLoaderData, useParams } from 'react-router-dom'
import { DashboardContent } from '~/components/DashboardContent'
import invariant from 'tiny-invariant'
import { useSearchParams } from 'react-router-dom'
import { formatDate } from '~/utils'
import { QUERY_PARAMS, loaderData, QueryLiterals } from './data'

import dayjs from 'dayjs'

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const [searchParams, setSearchParams] = useSearchParams()

  const getOnChangeDate = (dateType: QueryLiterals) => (dateValue: dayjs.Dayjs | null) => {
    setSearchParams(
      (params) => {
        params.delete(dateType)

        if (dateValue) {
          params.append(dateType, formatDate(dateValue.toDate()))
        }

        return params
      },
      { preventScrollReset: true, replace: true }
    )
  }

  const data = useLoaderData() as loaderData
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }

  const date_from = dayjs(searchParams.get(QUERY_PARAMS.FROM) || dataRanges.minDate)
  const date_to = dayjs(searchParams.get(QUERY_PARAMS.TO) || dataRanges.maxDate)

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
            onChange={getOnChangeDate(QUERY_PARAMS.FROM)}
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
            onChange={getOnChangeDate(QUERY_PARAMS.TO)}
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
