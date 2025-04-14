import dayjs, { type Dayjs } from 'dayjs'
import type { PlotMouseEvent } from 'plotly.js'
import { useEffect, useState } from 'react'
import {
  DateFilter,
  type DateFilterProps,
  type DateFilterState,
  ShowInOrderSwitch
} from '~/components/DashboardDateFilter'
import { DashboardViewParamsContext } from '~/contexts/DashboardViewParams'
import { useDebounce, useIsFirstRender, useLocalStorage } from '~/hooks/index'

export const ProjectDashboard = ({
  Widgets,
  dateFilterProps,
  OnClickedPointComponent,
  OnHoveredPlotComponent
}: {
  Widgets: React.ReactNode
  dateFilterProps: DateFilterProps
  OnClickedPointComponent?: ({ event }: { event: PlotMouseEvent }) => JSX.Element
  OnHoveredPlotComponent?: () => JSX.Element
}) => {
  const [isXaxisAsCategorical, setIsXaxisAsCategorical] = useLocalStorage(
    'dashboard-hide-dates',
    false
  )

  return (
    <>
      <DateFilter {...dateFilterProps} flexEnd>
        <ShowInOrderSwitch
          isXaxisAsCategorical={isXaxisAsCategorical}
          setIsXaxisAsCategorical={setIsXaxisAsCategorical}
        />
      </DateFilter>

      <DashboardViewParamsContext.Provider
        value={{ isXaxisAsCategorical, OnClickedPointComponent, OnHoveredPlotComponent }}
      >
        {Widgets}
      </DashboardViewParamsContext.Provider>
    </>
  )
}

export const getValidDate = (date?: string | null | Dayjs) =>
  date && dayjs(date).isValid() ? dayjs(date) : undefined

export const getDataRange = ({
  min_timestamp,
  max_timestamp
}: { min_timestamp?: string | null; max_timestamp?: string | null }) => {
  const [minDate, maxDate] = [getValidDate(min_timestamp), getValidDate(max_timestamp)]

  return { minDate, maxDate }
}

export const useDashboardFilterParamsDebounced = ({
  dates,
  onDebounce,
  delay = 300
}: {
  delay?: number
  dates: DateFilterState
  onDebounce: (d: DateFilterState) => void
}) => {
  const isFirstRender = useIsFirstRender()

  const [internalDates, setInternalDates] = useState<DateFilterState>(dates)

  const datesDebounced = useDebounce(internalDates, delay)

  // biome-ignore lint/correctness/useExhaustiveDependencies: fine
  useEffect(() => {
    if (isFirstRender) {
      return
    }

    onDebounce(datesDebounced)
  }, [datesDebounced])

  return {
    dates: internalDates,
    setDates: setInternalDates
  }
}
