import { RouteObject } from 'react-router'
import { Component, handle, loader } from './Component'
import TestSuiteRoute from './testSuiteId'

export default {
  id: 'test_suites',
  path: 'test-suites',
  Component,
  loader,
  handle,
  children: [TestSuiteRoute]
} satisfies RouteObject
