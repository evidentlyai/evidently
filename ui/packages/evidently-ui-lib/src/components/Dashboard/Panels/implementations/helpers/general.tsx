import { Box, Card, CardContent, Divider, type SxProps, Typography } from '@mui/material'
import type React from 'react'

export const PanelCardGeneral = ({
  title,
  description,
  height,
  children,
  sxCardContent,
  textCenterAlign,
  borderNone = false
}: {
  title?: string
  description?: string
  height?: number
  children?: React.ReactNode
  sxCardContent?: SxProps
  textCenterAlign?: boolean
  borderNone?: boolean
}) => {
  return (
    <Card elevation={0} sx={[borderNone && { border: 'none' }]}>
      <CardContent
        sx={[{ px: 0 }, ...(Array.isArray(sxCardContent) ? sxCardContent : [sxCardContent])]}
      >
        <Box px={3}>
          {title && (
            <Typography
              align={textCenterAlign ? 'center' : undefined}
              variant='h5'
              fontWeight={500}
              gutterBottom
            >
              {title}
            </Typography>
          )}

          {description && (
            <Typography
              align={textCenterAlign ? 'center' : undefined}
              fontWeight={400}
              gutterBottom
            >
              {description}
            </Typography>
          )}
        </Box>

        {(title || description) && children && <Divider sx={{ mb: 2, mt: 1 }} />}

        {children && (
          <Box height={height} px={3}>
            {children}
          </Box>
        )}
      </CardContent>
    </Card>
  )
}
