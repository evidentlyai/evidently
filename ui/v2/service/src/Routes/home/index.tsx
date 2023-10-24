import { RouteObject } from 'react-router-dom'

export default {
  path: '/',
  lazy: () => import('./Component')
} satisfies RouteObject
