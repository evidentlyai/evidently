import dayjs from 'dayjs'
import type { DashboardInfoModel } from '~/api/types'
import { useLocalStorage } from '~/hooks'

export const useDashboardParams = (data: DashboardInfoModel) => {
  const isShowDateFilter = data.min_timestamp !== null && data.max_timestamp !== null
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }
  const [isDashboardHideDates, setIsDashboardHideDates] = useLocalStorage(
    'dashboard-hide-dates',
    false
  )

  return { isShowDateFilter, dataRanges, isDashboardHideDates, setIsDashboardHideDates }
}
