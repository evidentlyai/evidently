import { Box, Card, CardContent, Divider, Skeleton, Typography } from '@mui/material'

export const DashboardPanelSkeleton = ({
  height = 350,
  title,
  subtitle,
  isShowTitle,
  skipBody
}: {
  isShowTitle?: boolean
  height?: number
  title?: string
  subtitle?: string
  skipBody?: boolean
}) => (
  <Card elevation={0}>
    <CardContent sx={{ px: 0 }}>
      <Box px={3}>
        {title && isShowTitle && (
          <Typography variant='h5' fontWeight={500} gutterBottom>
            {title}
          </Typography>
        )}

        {title && !isShowTitle && (
          <Typography variant='h5' width={Math.max(title.length * 11, 450)}>
            <Skeleton variant='text' animation='wave' sx={{ mb: 1 }} />
          </Typography>
        )}

        {subtitle && isShowTitle && (
          <Typography fontWeight={400} gutterBottom>
            {subtitle}
          </Typography>
        )}

        {subtitle && !isShowTitle && (
          <Typography>
            <Skeleton variant='text' animation='wave' sx={{ mb: 1 }} />
          </Typography>
        )}
      </Box>

      {(title || subtitle) && !skipBody && <Divider sx={{ mb: 2, mt: 1 }} />}

      {!skipBody && (
        <Box px={3}>
          <Skeleton variant='rectangular' height={height} animation='wave' />
        </Box>
      )}
    </CardContent>
  </Card>
)
