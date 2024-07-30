import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/dashboard/data'
import { clientAPI } from '~/api'

const { loader } = getLoaderAction({ api: clientAPI })

export default {
  index: true,
  id: 'dashboard',
  lazy: async () => {
    const [{ DashboardComponentTemplate }, { DashboardWidgets }] = await Promise.all([
      import('evidently-ui-lib/routes-components/dashboard'),
      import('evidently-ui-lib/components/DashboardWidgets')
    ])

    return {
      Component: () => (
        <DashboardComponentTemplate
          Dashboard={({ data: { widgets } }) => <DashboardWidgets widgets={widgets} />}
        />
      )
    }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
