import { createMuiTheme } from '@material-ui/core'

export const theme = createMuiTheme({
  shape: {
    borderRadius: 0
  },
  palette: {
    primary: {
      light: '#ed5455',
      main: '#ed0400',
      dark: '#d40400',
      contrastText: '#fff'
    },
    secondary: {
      light: '#61a0ff',
      main: '#3c7fdd',
      dark: '#61a0ff',
      contrastText: '#000'
    }
  },
  typography: {
    button: {
      fontWeight: 'bold'
    },
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
    ].join(',')
  }
})
