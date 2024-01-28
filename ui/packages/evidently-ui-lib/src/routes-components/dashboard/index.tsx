import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DashboardDateFilter, useIsCorrectTimeInterval } from '~/components/DashboardDateFilter'
import { loaderData } from './data'
import dayjs from 'dayjs'

interface Props {
  Dashboard: ({ data }: { data: loaderData }) => JSX.Element
}

export const DashboardComponentTemplate = ({ Dashboard }: Props) => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as loaderData
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }
  const { isCorrectTimeInterval } = useIsCorrectTimeInterval({ dataRanges })

  return (
    <>
      <DashboardDateFilter dataRanges={dataRanges} />

      {isCorrectTimeInterval && <Dashboard data={data} />}
    </>
  )
}
