import { RouteObject } from 'react-router-dom'

export default {
  index: true,
  id: 'dashboard',
  lazy: () => import('./Component')
} satisfies RouteObject
