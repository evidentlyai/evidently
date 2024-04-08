import { colors } from '@mui/material'
import { createTheme } from '@mui/material/styles'

const { transitions } = createTheme()

const mainRed = '#ed0500'
const borderColorGrey = '#ded5d5'

export const theme = createTheme({
  shape: { borderRadius: 5 },
  palette: {
    primary: { main: colors.grey[900] },
    // we use `secondary` color for interactive elements
    secondary: { main: mainRed, dark: '#c10400' },
    background: { default: 'white', paper: 'white' }
  },
  components: {
    MuiLink: {
      styleOverrides: {
        root: {
          transition: transitions.create('color', {
            duration: transitions.duration.enteringScreen
          }),
          '&:hover': {
            color: mainRed
          }
        }
      }
    },
    MuiTabs: {
      styleOverrides: { flexContainer: { gap: '10px' }, indicator: { backgroundColor: mainRed } }
    },
    MuiButton: {
      styleOverrides: {
        contained: {
          '&:hover': { background: colors.grey[800] }
        },
        outlined: {
          '&:hover': {
            color: mainRed,
            borderColor: mainRed,
            background: 'white'
          }
        },
        text: {
          '&:hover': {
            color: mainRed,
            borderColor: mainRed
          }
        }
      }
    },
    MuiTab: {
      defaultProps: { color: 'secondary' },
      styleOverrides: {
        root: {
          fontSize: '1rem',
          borderRadius: '5px',
          '&:hover': {
            background: colors.grey[200]
          }
        }
      }
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          transition: transitions.create('color', {
            duration: transitions.duration.enteringScreen
          }),
          color: colors.grey[900],
          '&:hover': {
            color: mainRed
          }
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
          color: colors.grey[900],
          '&:hover': {
            color: mainRed
          }
        }
      }
    },
    MuiToggleButtonGroup: { defaultProps: { color: 'secondary' } },
    MuiLinearProgress: { defaultProps: { color: 'secondary' } },
    MuiPaper: {
      styleOverrides: {
        root: { boxShadow: 'unset', border: '1px solid', borderColor: borderColorGrey }
      }
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
