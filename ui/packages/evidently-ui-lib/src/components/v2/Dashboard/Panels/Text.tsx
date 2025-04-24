import { Card, CardContent, Typography } from 'evidently-ui-lib/shared-dependencies/mui-material'

export type TextPanelProps = {
  plotType: 'text'
  title?: string
  description?: string
}

export const TextDashboardPanel = ({ title, description }: TextPanelProps) => {
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
      </CardContent>
    </Card>
  )
}
