import { useLoaderData, useParams } from 'react-router-dom'
import invariant from 'tiny-invariant'
import { DateTimeRangeByQueryParams } from '~/components/DashboardDateFilter'
import { LoaderData } from './data'
import { DashboardViewParamsContext } from '~/contexts/DashboardViewParams'
import { useLocalStorage } from '~/hooks'
import { Box, FormControlLabel, Switch } from '@mui/material'
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
  const [isDashboardHideDates, setIsDashboardHideDates] = useLocalStorage(
    'dashboard-hide-dates',
    false
  )

  return (
    <>
      <DateTimeRangeByQueryParams
        dataRanges={dataRanges}
        isShowDateFilter={isShowDateFilter}
        slot={
          <Box minWidth={180} display={'flex'} justifyContent={'center'}>
            <FormControlLabel
              control={
                <Switch
                  checked={isDashboardHideDates}
                  onChange={(event) => setIsDashboardHideDates(event.target.checked)}
                ></Switch>
              }
              label="Show in order"
            />
          </Box>
        }
      />

      <DashboardViewParamsContext.Provider value={{ isXaxisAsCategorical: isDashboardHideDates }}>
        <Dashboard data={data} />
      </DashboardViewParamsContext.Provider>
    </>
  )
}
