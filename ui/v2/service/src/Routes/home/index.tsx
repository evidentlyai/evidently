import { RouteObject } from 'react-router-dom'
import { Component, handle } from './Component'

////////////////////
// children routes
////////////////////

export default {
  path: '/',
  Component,
  handle
} satisfies RouteObject
