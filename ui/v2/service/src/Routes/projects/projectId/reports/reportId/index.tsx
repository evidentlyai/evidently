import { RouteObject } from 'react-router-dom'
import { Component, handle, loader } from './Component'

export default {
  id: 'show-report-by-id',
  path: ':reportId',
  Component,
  loader,
  handle
} satisfies RouteObject
