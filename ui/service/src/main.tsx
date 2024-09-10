import React from 'react'
import ReactDOM from 'react-dom/client'

import { ThemeProvider } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { RouterProvider } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { theme } from 'evidently-ui-lib/theme/v2'
import { router } from '~/Routes'
import './index.css'

const rootElement = document.getElementById('root')

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <RouterProvider router={router} />
      </ThemeProvider>
    </React.StrictMode>
  )
}
