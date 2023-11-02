import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui/routes-components/dashboard/data'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  index: true,
  id: 'dashboard',
  lazy: () => import('evidently-ui/routes-components/dashboard'),
  loader
} satisfies RouteObject
