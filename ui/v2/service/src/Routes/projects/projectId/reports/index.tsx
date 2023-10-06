import { RouteObject } from 'react-router-dom'
import { Component, handle, loader } from './Component'

////////////////////
// children routes
////////////////////

import ReportRoute from './reportId'

export default {
  id: 'reports',
  path: 'reports',
  loader,
  Component,
  handle,
  children: [ReportRoute]
} satisfies RouteObject
