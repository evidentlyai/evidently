import {
  Alert,
  AlertTitle,
  Box,
  Collapse,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Typography
} from '@mui/material'
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'

import dayjs, { Dayjs } from 'dayjs'
import 'dayjs/plugin/duration'

import { useSearchParams } from 'react-router-dom'
import { formatDate } from '~/utils'

type QueryAliases = 'FROM' | 'TO'
type QueryLiterals = 'date_from' | 'date_to'

export const FILTER_QUERY_PARAMS: Record<QueryAliases, QueryLiterals> = {
  FROM: 'date_from',
  TO: 'date_to'
}

interface DashboardDateFilterProps {
  dataRanges: { minDate: Dayjs; maxDate: Dayjs }
}

export const getDashboardQueryParams = (searchParams: URLSearchParams) => {
  let date_from = searchParams.get(FILTER_QUERY_PARAMS.FROM)
  let date_to = searchParams.get(FILTER_QUERY_PARAMS.TO)
  return { date_from, date_to }
}

export const useIsCorrectTimeInterval = ({ dataRanges }: DashboardDateFilterProps) => {
  const [searchParams, setSearchParams] = useSearchParams()

  const { date_from: dateFrom, date_to: dateTo } = getDashboardQueryParams(searchParams)

  const date_from = dayjs(dateFrom || dataRanges.minDate)
  const date_to = dayjs(dateTo || dataRanges.maxDate)

  const isCorrectTimeInterval =
    date_from.isValid() && date_to.isValid() && date_from.isBefore(date_to)

  return { isCorrectTimeInterval, date_from, date_to, setSearchParams }
}

export const DashboardDateFilter = ({ dataRanges }: DashboardDateFilterProps) => {
  const { isCorrectTimeInterval, date_from, date_to, setSearchParams } = useIsCorrectTimeInterval({
    dataRanges
  })

  const isIncorrectTimeIntervalMessage = !isCorrectTimeInterval ? 'incorrect time interval' : ''

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

  return (
    <Grid
      container
      padding={1}
      zIndex={1}
      // my={3}
      gap={2}
      justifyContent="flex-end"
      justifyItems={'center'}
    >
      <Grid item xs={12} md={2}>
        <FormControl fullWidth>
          <InputLabel>Period</InputLabel>
          <Select
            variant="standard"
            defaultValue={''}
            onChange={(event) => {
              const [valueStr, durationStr] = (event.target.value as string).split(',')

              if (valueStr === '') {
                setSearchParams(
                  (params) => {
                    params.delete(FILTER_QUERY_PARAMS.FROM)
                    params.delete(FILTER_QUERY_PARAMS.TO)

                    params.append(FILTER_QUERY_PARAMS.FROM, formatDate(dataRanges.minDate.toDate()))
                    params.append(FILTER_QUERY_PARAMS.TO, formatDate(dataRanges.maxDate.toDate()))

                    return params
                  },
                  { preventScrollReset: true, replace: true }
                )

                return
              }

              const [value, duration] = [Number(valueStr), durationStr]
              const lastDate = dataRanges.maxDate.subtract(value, duration as dayjs.ManipulateType)

              setSearchParams(
                (params) => {
                  params.delete(FILTER_QUERY_PARAMS.FROM)
                  params.delete(FILTER_QUERY_PARAMS.TO)

                  params.append(
                    FILTER_QUERY_PARAMS.FROM,
                    formatDate(
                      lastDate.isBefore(dataRanges.minDate)
                        ? dataRanges.minDate.toDate()
                        : lastDate.toDate()
                    )
                  )
                  params.append(FILTER_QUERY_PARAMS.TO, formatDate(dataRanges.maxDate.toDate()))

                  return params
                },
                { preventScrollReset: true, replace: true }
              )
            }}
          >
            <MenuItem value={''}>
              <em>None</em>
            </MenuItem>
            <MenuItem value={'10,minutes'}>Last 10 Minutes</MenuItem>
            <MenuItem value={'30,minutes'}>Last 30 Minutes</MenuItem>
            <MenuItem value={'1,hours'}>Last 1 Hours</MenuItem>
            <MenuItem value={'2,hours'}>Last 2 Hours</MenuItem>
            <MenuItem value={'8,hours'}>Last 8 Hours</MenuItem>
            <MenuItem value={'24,hours'}>Last 24 Hours</MenuItem>
            <MenuItem value={'7,days'}>Last 7 Days</MenuItem>
            <MenuItem value={'14,days'}>Last 14 Days</MenuItem>
            <MenuItem value={'28,days'}>Last 28 Days</MenuItem>
            <MenuItem value={'60,days'}>Last 60 Days</MenuItem>
          </Select>
        </FormControl>
      </Grid>
      <Grid item>
        <Box display={'flex'} alignItems={'center'} gap={2}>
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
            onChange={getOnChangeDate(FILTER_QUERY_PARAMS.FROM)}
          />
          <Box height={1} display={'flex'} alignItems={'center'}>
            <Typography> - </Typography>
          </Box>
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
            onChange={getOnChangeDate(FILTER_QUERY_PARAMS.TO)}
          />
        </Box>
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
  )
}
