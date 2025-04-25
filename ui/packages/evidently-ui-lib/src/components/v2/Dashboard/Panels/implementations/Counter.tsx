import type { SeriesModel } from 'evidently-ui-lib/api/types/v2'
import {
  Box,
  Card,
  CardContent,
  Divider,
  Grid2 as Grid,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'
import { jsonToKeyValueRowString } from '../../utils'

export type CounterPanelProps = MakePanel<{
  type: 'counter'
  size: 'full' | 'half'
  data: SeriesModel
  title?: string
  description?: string
  counterAgg: 'last' | 'sum' | 'avg'
}>

export const CounterDashboardPanel = ({
  data,
  title,
  description,
  counterAgg
}: CounterPanelProps) => {
  return (
    <Card elevation={0}>
      <CardContent sx={{ px: 0 }}>
        <Box px={3}>
          {title && (
            <Typography variant='h5' align='center' fontWeight={500} gutterBottom>
              {title}
            </Typography>
          )}

          {description && (
            <Typography fontWeight={400} align='center' gutterBottom>
              {description}
            </Typography>
          )}
        </Box>

        {(title || description) && <Divider sx={{ mb: 2, mt: 1 }} />}

        <Box sx={{ flexGrow: 1, px: 3 }}>
          <Grid container spacing={2} justifyContent={'space-evenly'}>
            {data.series.map(({ metric_type, params, values }) => (
              <Grid key={`${metric_type.split(':').at(-1)}\n${jsonToKeyValueRowString(params)}`}>
                <Box>
                  <Typography variant='h2' align={'center'}>
                    {getValue(values, counterAgg)?.toFixed(2)}
                  </Typography>
                  <Typography component={'pre'} align={'center'}>
                    {`${metric_type.split(':').at(-1)}\n${jsonToKeyValueRowString(params)}`}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Box>
      </CardContent>
    </Card>
  )
}

function getValue(data: (number | null)[], counterAgg: CounterPanelProps['counterAgg']) {
  if (data.length === 0) {
    return null
  }

  if (counterAgg === 'last') {
    return data[data.length - 1]
  }

  if (counterAgg === 'sum') {
    return data.reduce((prev, curr) => (prev ?? 0) + (curr ?? 0), 0)
  }

  if (counterAgg === 'avg') {
    return (data.reduce((prev, curr) => (prev ?? 0) + (curr ?? 0), 0) ?? 0) / data.length
  }
}
