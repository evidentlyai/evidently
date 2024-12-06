import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { GoToSnapshotByPoint, HintOnHoverToPlot } from 'evidently-ui-lib/components/OnClickedPoint'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/dashboard/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
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
          OnClickedPointComponent={GoToSnapshotByPoint}
          OnHoveredPlotComponent={HintOnHoverToPlot}
        />
      )
    }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
