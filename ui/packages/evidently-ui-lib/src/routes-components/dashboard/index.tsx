import dayjs from 'dayjs'
import type { PlotMouseEvent } from 'plotly.js'
import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardParams } from '~/components/DashboardDateFilter'
import { DashboardViewParamsContext } from '~/contexts/DashboardViewParams'
import { useLocalStorage } from '~/hooks'
import type { LoaderData } from './data'

interface Props {
  Dashboard: ({ data }: { data: LoaderData }) => JSX.Element
  OnClickedPointComponent?: ({ event }: { event: PlotMouseEvent }) => JSX.Element
  OnHoveredPlotComponent?: () => JSX.Element
}

export const DashboardComponentTemplate = ({
  Dashboard,
  OnClickedPointComponent,
  OnHoveredPlotComponent
}: Props) => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as LoaderData

  const isShowDateFilter = data.min_timestamp !== null && data.max_timestamp !== null
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }
  const [isDashboardHideDates, setIsDashboardHideDates] = useLocalStorage(
    'dashboard-hide-dates',
    false
  )

  return (
    <>
      <DashboardParams
        dataRanges={dataRanges}
        isShowDateFilter={isShowDateFilter}
        isDashboardHideDates={isDashboardHideDates}
        setIsDashboardHideDates={setIsDashboardHideDates}
      />

      <DashboardViewParamsContext.Provider
        value={{
          isXaxisAsCategorical: isDashboardHideDates,
          OnClickedPointComponent,
          OnHoveredPlotComponent
        }}
      >
        <Dashboard data={data} />
      </DashboardViewParamsContext.Provider>
    </>
  )
}
