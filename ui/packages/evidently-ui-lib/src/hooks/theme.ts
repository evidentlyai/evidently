import { useColorScheme, useMediaQuery } from '@mui/material'
import { useMemo } from 'react'

export const useThemeMode = () => {
  const { mode } = useColorScheme()
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)')

  return !mode || mode === 'system' ? (prefersDarkMode ? 'dark' : 'light') : mode
}

export const useNivoTheme = () => {
  const mode = useThemeMode()

  const theme = useMemo(
    () =>
      mode === 'dark'
        ? {
            tooltip: {
              container: {
                background: '#000',
                color: '#fff'
              }
            }
          }
        : undefined,
    [mode]
  )

  return theme
}
