import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'

import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Routes } from 'Routes'
import { ThemeProvider } from '@mui/material'
import { theme } from 'evidently-ui-lib/theme/v1'

const router = createBrowserRouter(Routes)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>
  </React.StrictMode>
)
