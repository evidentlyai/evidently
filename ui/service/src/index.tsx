import ReactDOM from 'react-dom'
import './index.css'

import reportWebVitals from './reportWebVitals'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

import { Routes } from './Routes'

const router = createBrowserRouter(Routes)

ReactDOM.render(
  <>
    <RouterProvider router={router} />
  </>,
  document.getElementById('root') as HTMLElement
)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals()
