import {
  Card,
  CardContent,
  Divider,
  Skeleton,
  Typography
} from 'evidently-ui-lib/shared-dependencies/mui-material'

export const DashboardPanelSkeleton = ({
  height = 350,
  title,
  subtitle
}: { height?: number; title?: string; subtitle?: string }) => {
  return (
    <Card elevation={0}>
      <CardContent>
        {title && (
          <Typography variant='h5' width={Math.max(title.length * 11, 450)}>
            <Skeleton variant='text' animation='wave' />
          </Typography>
        )}

        {subtitle && (
          <Typography>
            <Skeleton variant='text' animation='wave' />
          </Typography>
        )}

        {(title || subtitle) && <Divider sx={{ mb: 2, mt: 1 }} />}

        <Skeleton
          // sx={{ borderRadius: 1 }}
          variant='rectangular'
          height={height}
          animation='wave'
        />
      </CardContent>
    </Card>
  )
}
