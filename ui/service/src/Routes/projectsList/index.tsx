import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui/routes-components/projectsList/data'
import { api } from 'api/RemoteApi'

const { loader, action } = injectAPI({ api })

export default {
  index: true,
  lazy: () => import('evidently-ui/routes-components/projectsList'),
  loader,
  action
} satisfies RouteObject
