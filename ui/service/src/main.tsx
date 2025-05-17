import React from 'react'
import ReactDOM from 'react-dom/client'

import { CssBaseline, ThemeProvider } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { RouterProvider } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { theme } from 'evidently-ui-lib/theme/index'
import { router } from './routes/router'

import './index.css'

const rootElement = document.getElementById('root')

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ThemeProvider
        theme={theme}
        // @ts-ignore // TODO: check new version of MUI
        forceThemeRerender
      >
        <CssBaseline />
        <RouterProvider router={router} />
      </ThemeProvider>
    </React.StrictMode>
  )
}
