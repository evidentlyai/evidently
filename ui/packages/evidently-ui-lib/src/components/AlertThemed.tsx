import { Alert, type AlertProps } from '@mui/material'
import { useThemeMode } from '~/hooks/theme'

export const AlertThemed: React.FC<Omit<AlertProps, 'variant'> & { forseFilled?: boolean }> = ({
  forseFilled,
  ...props
}) => {
  const mode = useThemeMode()

  return (
    <Alert
      variant={mode === 'dark' ? (forseFilled ? 'filled' : 'outlined') : undefined}
      {...props}
    />
  )
}
