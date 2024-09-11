import {
  Alert,
  AlertTitle,
  Box,
  Collapse,
  FormControl,
  FormControlLabel,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Switch,
  Typography
} from '@mui/material'

import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker'

import dayjs, { type Dayjs } from 'dayjs'
import 'dayjs/locale/en-gb'
import 'dayjs/plugin/duration'

import { LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useDebounce, useIsFirstRender } from '~/hooks'
import { formatDate } from '~/utils'

type QueryAliases = 'FROM' | 'TO'
type QueryLiterals = 'date_from' | 'date_to'

export const FILTER_QUERY_PARAMS: Record<QueryAliases, QueryLiterals> = {
  FROM: 'date_from',
  TO: 'date_to'
}

interface DataRangesProps {
  dataRanges: { minDate: Dayjs; maxDate: Dayjs }
}

interface DashboardDateFilterProps {
  isShowDateFilter: boolean
  isDashboardHideDates: boolean
  setIsDashboardHideDates: React.Dispatch<React.SetStateAction<boolean>>
}

export const getDashboardQueryParams = (searchParams: URLSearchParams) => {
  const date_from = searchParams.get(FILTER_QUERY_PARAMS.FROM)
  const date_to = searchParams.get(FILTER_QUERY_PARAMS.TO)
  return { date_from, date_to }
}

export const useIsCorrectTimeInterval = ({ dataRanges }: DataRangesProps) => {
  const [searchParams, setSearchParams] = useSearchParams()

  const { date_from: dateFrom, date_to: dateTo } = getDashboardQueryParams(searchParams)

  const date_from = dayjs(dateFrom || dataRanges.minDate)
  const date_to = dayjs(dateTo || dataRanges.maxDate)

  const isCorrectTimeInterval =
    date_from.isValid() &&
    date_to.isValid() &&
    (date_from.isSame(date_to) || date_from.isBefore(date_to))

  return { isCorrectTimeInterval, date_from, date_to, setSearchParams }
}

export const DashboardParams = ({
  dataRanges,
  isDashboardHideDates,
  setIsDashboardHideDates,
  isShowDateFilter
}: DashboardDateFilterProps & DataRangesProps) => {
  const isFirstRender = useIsFirstRender()
  const { isCorrectTimeInterval, date_from, date_to, setSearchParams } = useIsCorrectTimeInterval({
    dataRanges
  })

  const [innerDatesState, setInnerStateDates] = useState<{
    date_from: Dayjs | null
    date_to: Dayjs | null
  }>({ date_from, date_to })

  const innerDatesStateDebounced = useDebounce(innerDatesState, 300)

  const isIncorrectTimeIntervalMessage = !isCorrectTimeInterval ? 'incorrect time interval' : ''

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (isFirstRender) {
      return
    }

    const date_to = innerDatesStateDebounced?.date_to?.toDate()
    const date_from = innerDatesStateDebounced?.date_from?.toDate()

    setSearchParams(
      (params) => {
        params.delete(FILTER_QUERY_PARAMS.FROM)
        params.delete(FILTER_QUERY_PARAMS.TO)

        date_from && params.append(FILTER_QUERY_PARAMS.FROM, formatDate(date_from))
        date_to && params.append(FILTER_QUERY_PARAMS.TO, formatDate(date_to))

        return params
      },
      { preventScrollReset: true, replace: true }
    )
  }, [innerDatesStateDebounced])

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <Grid
        container
        padding={1}
        zIndex={1}
        gap={2}
        justifyContent='flex-end'
        alignItems={'flex-end'}
      >
        <Grid item>
          <Box minWidth={180} display={'flex'} justifyContent={'center'}>
            <FormControlLabel
              control={
                <Switch
                  checked={isDashboardHideDates}
                  onChange={(event) => setIsDashboardHideDates(event.target.checked)}
                />
              }
              label='Show in order'
            />
          </Box>
        </Grid>
        {isShowDateFilter && (
          <>
            <Grid item xs={12} md={2}>
              <FormControl fullWidth>
                <InputLabel>Period</InputLabel>
                <Select
                  variant='standard'
                  defaultValue={''}
                  onChange={(event) => {
                    const [valueStr, durationStr] = (event.target.value as string).split(',')

                    if (valueStr === '') {
                      setInnerStateDates({ date_from: null, date_to: null })

                      return
                    }

                    const [value, duration] = [Number(valueStr), durationStr]
                    const lastDate = dataRanges.maxDate.subtract(
                      value,
                      duration as dayjs.ManipulateType
                    )

                    setInnerStateDates({
                      date_from: lastDate.isBefore(dataRanges.minDate)
                        ? dataRanges.minDate
                        : lastDate,
                      date_to: dataRanges.maxDate
                    })
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
                  label='From'
                  value={innerDatesState.date_from}
                  onChange={(date_from) => setInnerStateDates((prev) => ({ ...prev, date_from }))}
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
                  label='To'
                  value={innerDatesState.date_to}
                  onChange={(date_to) => setInnerStateDates((prev) => ({ ...prev, date_to }))}
                />
              </Box>
            </Grid>
            <Grid item xs={12}>
              <Collapse unmountOnExit in={!isCorrectTimeInterval}>
                <Alert severity='error'>
                  <AlertTitle>Error</AlertTitle>
                  {isIncorrectTimeIntervalMessage}
                </Alert>
              </Collapse>
            </Grid>
          </>
        )}
      </Grid>
    </LocalizationProvider>
  )
}

export type DateFilterState = {
  dateFrom?: Dayjs | null
  dateTo?: Dayjs | null
}

export interface DateFilterProps {
  dates: DateFilterState
  setDates: React.Dispatch<React.SetStateAction<DateFilterState>>
  required?: boolean
}

export const DateFilter = ({ dates, setDates, required = false }: DateFilterProps) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={'en-gb'}>
      <Grid
        container
        padding={1}
        zIndex={1}
        gap={2}
        justifyContent='flex-start'
        alignItems={'flex-end'}
      >
        <>
          <Grid item xs={12} md={2}>
            <FormControl fullWidth>
              <InputLabel>Period</InputLabel>
              <Select
                variant='standard'
                defaultValue={''}
                onChange={(event) => {
                  const [valueStr, durationStr] = (event.target.value as string).split(',')

                  if (valueStr === '') {
                    setDates({ dateFrom: null, dateTo: null })
                    return
                  }

                  const now = dayjs()
                  const [value, duration] = [Number(valueStr), durationStr]
                  const lastDate = now.subtract(value, duration as dayjs.ManipulateType)

                  setDates({ dateFrom: lastDate, dateTo: now })
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
                minDate={undefined}
                maxDate={dates?.dateTo}
                slotProps={{
                  textField: {
                    variant: 'standard',
                    error: required ? !dates.dateFrom : undefined
                  }
                }}
                label='From'
                value={dates?.dateFrom}
                onChange={(value) => setDates((prev) => ({ ...prev, dateFrom: value }))}
              />
              <Box height={1} display={'flex'} alignItems={'center'}>
                <Typography> - </Typography>
              </Box>
              <DateTimePicker
                minDate={dates?.dateFrom}
                maxDate={undefined}
                slotProps={{
                  textField: {
                    variant: 'standard',
                    error: required ? !dates.dateTo : undefined
                  }
                }}
                label='To'
                value={dates?.dateTo}
                onChange={(value) => setDates((prev) => ({ ...prev, dateTo: value }))}
              />
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Collapse
              unmountOnExit
              in={Boolean(dates.dateFrom && dates.dateTo && dates.dateFrom?.isAfter(dates.dateTo))}
            >
              <Alert severity='error'>
                <AlertTitle>Error</AlertTitle>
                Incorrect time interval
              </Alert>
            </Collapse>
          </Grid>
        </>
      </Grid>
    </LocalizationProvider>
  )
}
