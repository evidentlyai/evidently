import { Card, CardContent, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { MakePanel } from '~/components/v2/Dashboard/Panels/types'

export type TextPanelProps = MakePanel<{
  type: 'text'
  size: 'full' | 'half'
  title?: string
  description?: string
}>

export const TextDashboardPanel = ({ title, description }: TextPanelProps) => {
  return (
    <Card elevation={0}>
      <CardContent sx={{ p: '16px !important' }}>
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
      </CardContent>
    </Card>
  )
}
