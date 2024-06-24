import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardParams } from '~/components/DashboardDateFilter'
import { loaderData } from './data'
import { DashboardViewParamsContext } from '~/contexts/DashboardViewParams'
import { useLocalStorage } from '~/hooks'
import dayjs from 'dayjs'

interface Props {
  Dashboard: ({ data }: { data: loaderData }) => JSX.Element
}

export const DashboardComponentTemplate = ({ Dashboard }: Props) => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as loaderData

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

      <DashboardViewParamsContext.Provider value={{ isXaxisAsCategorical: isDashboardHideDates }}>
        <Dashboard data={data} />
      </DashboardViewParamsContext.Provider>
    </>
  )
}
