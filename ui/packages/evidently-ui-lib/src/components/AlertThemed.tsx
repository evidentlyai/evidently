import { Alert, type AlertProps } from '@mui/material'
import { alertClasses } from '@mui/material/Alert'
import { useThemeMode } from '~/hooks/theme'

export const AlertThemed: React.FC<Omit<AlertProps, 'variant'> & { forseFilled?: boolean }> = ({
  forseFilled,
  sx,
  ...props
}) => {
  const mode = useThemeMode()

  return (
    <Alert
      sx={[
        (theme) => theme.applyStyles('light', { border: 'none' }),
        ...(Array.isArray(sx) ? sx : [sx]),
        { [`& .${alertClasses.icon}`]: { alignItems: 'center' } }
      ]}
      variant={mode === 'dark' ? (forseFilled ? 'filled' : 'outlined') : undefined}
      {...props}
    />
  )
}
