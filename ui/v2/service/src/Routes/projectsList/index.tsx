import { RouteObject } from 'react-router-dom'

export default {
  index: true,
  lazy: () => import('./Component')
} satisfies RouteObject
