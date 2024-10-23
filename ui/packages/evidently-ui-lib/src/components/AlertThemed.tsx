import { Alert, type AlertProps } from '@mui/material'
import { useThemeMode } from '~/hooks/theme'

export const AlertThemed: React.FC<Omit<AlertProps, 'variant'>> = ({ ...props }) => {
  const mode = useThemeMode()

  return <Alert variant={mode === 'dark' ? 'outlined' : undefined} {...props} />
}
