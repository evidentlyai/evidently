import { RouteObject } from 'react-router-dom'
import { injectAPI } from 'evidently-ui-lib/routes-components/dashboard/data'
import { DashboardWidgets } from 'evidently-ui-lib/components/DashboardWidgets'
import { api } from 'api/RemoteApi'

const { loader } = injectAPI({ api })

export default {
  index: true,
  id: 'dashboard',
  lazy: async () => {
    const { DashboardComponentTemplate } = await import(
      'evidently-ui-lib/routes-components/dashboard'
    )

    return {
      Component: () => (
        <DashboardComponentTemplate
          Dashboard={({ data: { widgets } }) => <DashboardWidgets widgets={widgets} />}
        />
      )
    }
  },
  loader
} satisfies RouteObject
