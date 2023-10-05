import { RouteObject } from 'react-router-dom'
import { Component, errorElement, action, loader } from './Component'

export default {
  index: true,
  loader,
  action,
  Component,
  errorElement
} satisfies RouteObject
