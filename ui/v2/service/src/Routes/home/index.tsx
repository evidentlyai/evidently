import { RouteObject } from 'react-router-dom'

////////////////////
// children routes
////////////////////

export default {
  path: '/',
  lazy: () => import('./Component')
} satisfies RouteObject
