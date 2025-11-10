import { useTheme } from '@mui/material'
import JsonView, { type JsonViewProps } from '@uiw/react-json-view'
import { githubDarkTheme } from '@uiw/react-json-view/githubDark'
import { githubLightTheme } from '@uiw/react-json-view/githubLight'
import { useMemo } from 'react'
import { useThemeMode } from '~/hooks/theme'

export const JsonViewThemed: React.FC<
  React.PropsWithRef<
    Omit<JsonViewProps<object>, 'style' | 'displayObjectSize' | 'displayDataTypes'>
  >
> = ({ ...props }) => {
  const mode = useThemeMode()

  const {
    vars: {
      palette: {
        primary: { main }
      }
    }
  } = useTheme()

  const theme = useMemo(
    () => ({
      ...(mode === 'light' ? githubLightTheme : githubDarkTheme),
      '--w-rjv-background-color': 'transparent',
      '--w-rjv-ellipsis-color': main
    }),
    [mode, main]
  )

  return <JsonView {...props} style={theme} displayObjectSize={false} displayDataTypes={false} />
}
