import type { SeriesModel } from 'evidently-ui-lib/api/types'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { PanelCardGeneral } from './helpers/general'
import { getAggValue, getLabel } from './helpers/utils'

export type CounterPanelProps = MakePanel<{
  type: 'counter'
  size: 'full' | 'half'
  labels: (string | undefined | null)[]
  data: SeriesModel
  title?: string
  description?: string
  aggregation: 'last' | 'sum' | 'avg'
}>

export const CounterDashboardPanel = ({
  data,
  labels,
  title,
  description,
  aggregation
}: CounterPanelProps) => {
  return (
    <PanelCardGeneral title={title} description={description} textCenterAlign>
      <Box>
        <Grid container spacing={2} justifyContent={'space-evenly'}>
          {data.series.map(({ metric_type, params, values, filter_index }, index) => {
            const { label, defaultLabel } = getLabel({ metric_type, params, labels, filter_index })

            const value = getAggValue(values, aggregation)

            return (
              <Grid key={`${index}:${defaultLabel}`}>
                <Box>
                  <Typography variant='h2' align={'center'}>
                    {value}
                  </Typography>
                  <Typography component={'pre'} align={'center'}>
                    {label}
                  </Typography>
                </Box>
              </Grid>
            )
          })}
        </Grid>
      </Box>
    </PanelCardGeneral>
  )
}
