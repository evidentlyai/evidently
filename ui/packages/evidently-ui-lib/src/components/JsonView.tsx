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

  const theme = useMemo(
    () => ({
      ...(mode === 'light' ? githubLightTheme : githubDarkTheme),
      '--w-rjv-background-color': 'transparent'
    }),
    [mode]
  )

  return <JsonView {...props} style={theme} displayObjectSize={false} displayDataTypes={false} />
}
