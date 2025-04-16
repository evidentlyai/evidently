import type { SeriesModel } from 'api/types'
import {
  Box,
  Card,
  CardContent,
  Divider,
  Grid2 as Grid,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'

type PanelProps = {
  data: SeriesModel
  plotType: 'text' | 'counter'
  isStacked?: boolean
  title?: string
  description?: string
  height?: number
  legendMarginRight?: number
  counterAgg?: 'last' | 'sum' | 'avg'
}

function getValue(data: number[], counterAgg: 'last' | 'sum' | 'avg') {
  if (data.length === 0) {
    return undefined
  }
  if (counterAgg === 'last') {
    return data[data.length - 1]
  }
  if (counterAgg === 'sum') {
    return data.reduce((prev, curr) => prev + curr, 0)
  }
  if (counterAgg === 'avg') {
    return data.reduce((prev, curr) => prev + curr, 0) / data.length
  }
}

export const CustomDashboardPanel = ({
  data,
  plotType,
  title,
  description,
  counterAgg
}: PanelProps) => {
  return (
    <Card elevation={0}>
      <CardContent>
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

        {(title || description) && plotType === 'counter' && <Divider sx={{ mb: 2, mt: 1 }} />}
        {plotType === 'counter' && (
          <Box sx={{ flexGrow: 1 }}>
            <Grid container spacing={2} justifyContent={'space-evenly'}>
              {data.series.map((s) => (
                <Grid
                  key={`${s.metric_type.split(':').at(-1)}\n${jsonToKeyValueRowString(s.params)}`}
                >
                  <Box>
                    <Typography variant='h2' align={'center'}>
                      {getValue(s.values, counterAgg ?? 'last')?.toPrecision(3)}
                    </Typography>
                    <Typography component={'pre'} align={'center'}>
                      {`${s.metric_type.split(':').at(-1)}\n${jsonToKeyValueRowString(s.params)}`}
                    </Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </CardContent>
    </Card>
  )
}

// biome-ignore lint/complexity/noBannedTypes: fine
const jsonToKeyValueRowString = (o: Object) => {
  const result = Object.entries(o)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n')

  return result
}
