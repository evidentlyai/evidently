import { Grid } from '@mui/material'

import dayjs from 'dayjs'
import 'dayjs/plugin/duration'

import { LoaderFunctionArgs, useLoaderData, useParams } from 'react-router-dom'
import { DashboardContent } from 'evidently-ui/components/DashboardContent'
import { api } from 'api/RemoteApi'
import invariant from 'tiny-invariant'
import {
  DashboardDateFilter,
  getDashboardQueryParams,
  useIsCorrectTimeInterval
} from 'Components/DashboardDateFilter'

export const loader = async ({ params, request }: LoaderFunctionArgs) => {
  invariant(params.projectId, 'missing projectId')

  const { searchParams } = new URL(request.url)

  let { date_from, date_to } = getDashboardQueryParams(searchParams)

  if (date_from && !dayjs(date_from).isValid()) {
    date_from = null
  }

  if (date_to && !dayjs(date_to).isValid()) {
    date_to = null
  }

  return api.getProjectDashboard(params.projectId, date_from, date_to, request.signal)
}

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as Awaited<ReturnType<typeof loader>>
  const dataRanges = { minDate: dayjs(data.min_timestamp), maxDate: dayjs(data.max_timestamp) }

  const { isCorrectTimeInterval } = useIsCorrectTimeInterval({ dataRanges })

  return (
    <>
      <DashboardDateFilter dataRanges={dataRanges} />

      {isCorrectTimeInterval && (
        <Grid container spacing={3} direction="row" alignItems="stretch">
          <DashboardContent info={data} />
        </Grid>
      )}
    </>
  )
}
