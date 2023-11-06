import { Grid } from '@mui/material'
import { useLoaderData, useParams } from 'react-router-dom'
import { DashboardContent } from '~/components/DashboardContent'
import invariant from 'tiny-invariant'
import { DashboardDateFilter, useIsCorrectTimeInterval } from '~/components/DashboardDateFilter'
import dayjs from 'dayjs'

import { loaderData } from './data'

export const Component = () => {
  const { projectId } = useParams()
  invariant(projectId, 'missing projectId')

  const data = useLoaderData() as loaderData

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
