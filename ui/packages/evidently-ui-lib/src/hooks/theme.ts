import { useColorScheme, useMediaQuery } from '@mui/material'

export const useThemeMode = () => {
  const { mode } = useColorScheme()
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)')

  return !mode || mode === 'system' ? (prefersDarkMode ? 'dark' : 'light') : mode
}
