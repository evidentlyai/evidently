import type { SeriesModel } from 'evidently-ui-lib/api/types/v2'
import { Box, Grid, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { formatLabelWithParams, jsonToKeyValueRowString } from '~/components/v2/Dashboard/utils'
import { PanelCardGeneral } from './helpers/general'
import { getAggValue } from './helpers/utils'

export type CounterPanelProps = MakePanel<{
  type: 'counter'
  size: 'full' | 'half'
  labels: (string | undefined | null)[]
  data: SeriesModel
  title?: string
  description?: string
  counterAgg: 'last' | 'sum' | 'avg'
}>

export const CounterDashboardPanel = ({
  data,
  labels,
  title,
  description,
  counterAgg
}: CounterPanelProps) => {
  return (
    <PanelCardGeneral title={title} description={description} textCenterAlign>
      <Box>
        <Grid container spacing={2} justifyContent={'space-evenly'}>
          {data.series.map(({ metric_type, params, values, filter_index }, index) => {
            const metricName = metric_type.split(':').at(-1)

            const defaultLabel = [metricName, jsonToKeyValueRowString(params)]
              .filter(Boolean)
              .join('\n')

            const customLabel = formatLabelWithParams({
              label: labels?.[filter_index] ?? '',
              params
            })

            const label = customLabel || defaultLabel

            const value = getAggValue(values, counterAgg)

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
