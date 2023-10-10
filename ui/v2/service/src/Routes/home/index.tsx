import { RouteObject } from 'react-router-dom'
import { Component, handle, loader } from './Component'

////////////////////
// children routes
////////////////////

export default {
  path: '/',
  Component,
  handle,
  loader
} satisfies RouteObject
