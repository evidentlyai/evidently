import { useDebounce, useIsFirstRender } from '@uidotdev/usehooks'
import dayjs from 'dayjs'
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import type { DateFilterState } from '~/components/DashboardDateFilter'
import { formatDate } from '~/utils'

export const DASHBOARD_DATE_FILTER_QUERY_PARAMS = { date_from: 'date_from', date_to: 'date_to' }

export const getDateFromSearch = (searchParams: URLSearchParams): DateFilterState => {
  const { date_from, date_to } = Object.fromEntries(searchParams)

  const getValidDate = (d: string) => (d && dayjs(d).isValid() && dayjs(d)) || null

  return { dateFrom: getValidDate(date_from), dateTo: getValidDate(date_to) }
}

export const getDateFromSearchForAPI = (searchParams: URLSearchParams) => {
  const { dateFrom, dateTo } = getDateFromSearch(searchParams)

  // TODO: remove using `formatDate`, just ISO format
  return {
    timestamp_start: (dateFrom && formatDate(dateFrom.toDate())) ?? null,
    timestamp_end: (dateTo && formatDate(dateTo.toDate())) ?? null
  }
}

export const useDashboardFilterPropsFromSearchParamsDebounced = ({
  min_timestamp,
  max_timestamp
}: { min_timestamp?: string | null; max_timestamp?: string | null }) => {
  const isFirstRender = useIsFirstRender()

  const dateRange = {
    ...(dayjs(min_timestamp ?? null).isValid()
      ? {
          minDate: dayjs(min_timestamp)
        }
      : null),
    ...(dayjs(max_timestamp ?? null).isValid()
      ? {
          maxDate: dayjs(max_timestamp)
        }
      : null)
  }

  const [searchParams, setSearchParams] = useSearchParams()

  const [dates, setDates] = useState<DateFilterState>(() => {
    const dfs = getDateFromSearch(searchParams)
    return {
      dateFrom: dfs.dateFrom ?? dateRange.minDate,
      dateTo: dfs.dateTo ?? dateRange.maxDate
    }
  })

  const datesDebounced = useDebounce(dates, 300)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (isFirstRender) {
      return
    }

    setSearchParams(
      (p) => ({
        ...Object.fromEntries(
          Object.entries(p).filter(([k]) => !(k in DASHBOARD_DATE_FILTER_QUERY_PARAMS))
        ),
        ...(datesDebounced.dateFrom?.isValid()
          ? {
              [DASHBOARD_DATE_FILTER_QUERY_PARAMS.date_from]: datesDebounced.dateFrom.toISOString()
            }
          : null),
        ...(datesDebounced.dateTo?.isValid()
          ? {
              [DASHBOARD_DATE_FILTER_QUERY_PARAMS.date_to]: datesDebounced.dateTo.toISOString()
            }
          : null)
      }),
      {
        replace: true,
        preventScrollReset: true
      }
    )
  }, [datesDebounced])

  return {
    dateRange,
    dates,
    setDates
  }
}
