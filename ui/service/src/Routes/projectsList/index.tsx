import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/projectsList/data'
import { api } from 'api/RemoteApi'

const { loader, action } = injectAPI({ api })

export default {
  index: true,
  lazy: () => import('evidently-ui-lib/routes-components/projectsList'),
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
