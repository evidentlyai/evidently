import { RouteObject } from 'react-router'
import { Component, handle, loader } from './Component'

export default {
  id: 'show-test-suite-by-id',
  path: ':testSuiteId',
  loader,
  Component,
  handle
} satisfies RouteObject
