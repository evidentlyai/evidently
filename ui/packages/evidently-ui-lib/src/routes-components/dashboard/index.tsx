import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardDateFilter } from '~/components/DashboardDateFilter'
import { LoaderData } from './data'
import dayjs from 'dayjs'

interface Props {
  Dashboard: ({ data }: { data: LoaderData }) => JSX.Element
}

export const DashboardComponentTemplate = ({ Dashboard }: Props) => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as LoaderData

  const isShowDateFilter = data.min_timestamp !== null && data.max_timestamp !== null
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }

  return (
    <>
      {isShowDateFilter && <DashboardDateFilter dataRanges={dataRanges} />}
      <Dashboard data={data} />
    </>
  )
}
