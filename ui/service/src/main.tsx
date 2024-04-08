import React from 'react'
import ReactDOM from 'react-dom/client'

import { RouterProvider } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { ThemeProvider } from 'evidently-ui-lib/shared-dependencies/mui-material'
import { theme } from 'evidently-ui-lib/theme/v2'
import { router } from 'Routes'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
)
