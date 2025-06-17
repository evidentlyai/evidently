import { colors } from '@mui/material'
import { createTheme } from '@mui/material/styles'

const { transitions } = createTheme()

const mainRed = '#ed0500'

declare module '@mui/material/styles' {
  interface CssThemeVariables {
    enabled: true
  }
}

export const theme = createTheme({
  cssVariables: { colorSchemeSelector: 'class' },
  colorSchemes: {
    light: {
      palette: {
        text: { primary: '#09090b' },
        primary: { main: '#09090b', light: colors.grey[200] },
        secondary: { main: mainRed, dark: '#c10400', light: colors.grey[200] }
      }
    },
    dark: {
      palette: {
        text: { primary: '#fafafa' },
        primary: { main: '#fafafa', light: colors.grey[900] },
        secondary: { main: mainRed }
      }
    }
  },
  shape: { borderRadius: 5 },
  components: {
    MuiInputBase: {
      styleOverrides: {
        input: {
          '&:-webkit-autofill': {
            transitionDelay: '9999s',
            transitionProperty: 'background-color, box-shadow, color'
          }
        }
      }
    },
    MuiLink: {
      styleOverrides: {
        root: {
          transition: transitions.create('color', {
            duration: transitions.duration.enteringScreen
          }),
          '&:hover': { color: mainRed }
        }
      }
    },
    MuiTabs: {
      styleOverrides: {
        flexContainer: { gap: '10px' },
        indicator: { backgroundColor: mainRed }
      }
    },
    MuiTab: {
      defaultProps: { color: 'secondary' },
      styleOverrides: {
        root: { fontSize: '1rem', borderRadius: '5px' }
      }
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          transition: transitions.create('color', {
            duration: transitions.duration.enteringScreen
          }),
          color: 'inherit',
          '&:hover': { color: mainRed }
        }
      }
    },
    MuiSwitch: { defaultProps: { color: 'secondary' } },
    MuiToggleButton: {
      defaultProps: { color: 'secondary' },
      styleOverrides: {
        root: {
          transition: transitions.create('color', {
            duration: transitions.duration.enteringScreen
          }),
          color: 'inherit',
          '&.Mui-disabled': { border: 'unset' }
        }
      }
    },
    MuiLinearProgress: { defaultProps: { color: 'secondary' } },
    MuiPaper: {
      defaultProps: { sx: { border: '1px solid', borderColor: 'divider' } },
      styleOverrides: { root: { boxShadow: 'unset' } }
    }
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"'
    ].join(','),
    button: {
      fontWeight: 'bold',
      textTransform: 'none'
    }
  }
})
