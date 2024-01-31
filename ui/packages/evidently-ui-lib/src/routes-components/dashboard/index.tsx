import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardDateFilter } from '~/components/DashboardDateFilter'
import { loaderData } from './data'
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

  return (
    <>
      {isShowDateFilter && <DashboardDateFilter dataRanges={dataRanges} />}
      <Dashboard data={data} />
    </>
  )
}
