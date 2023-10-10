import { RouteObject } from 'react-router-dom'
import { Component, handle, loader } from './Component'

////////////////////
// children routes
////////////////////

import DashboardRoute from './dashboard'
import ReportsRoute from './reports'
import TestSuitesRoute from './test-suites'
import TestSuitesOldRoute from './test_suites'

export default {
  path: 'projects/:projectId',
  loader,
  Component,
  handle,
  children: [DashboardRoute, ReportsRoute, TestSuitesRoute, TestSuitesOldRoute]
} satisfies RouteObject
