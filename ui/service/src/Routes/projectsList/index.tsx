import { ActionsErrorSnackbar, GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/projectsList/data'
import { clientAPI } from '~/api'

const { loader, action } = getLoaderAction({ api: clientAPI })

export default {
  index: true,
  lazy: () =>
    import('evidently-ui-lib/routes-components/projectsList').then((e) => ({
      ...e,
      Component: () => (
        <>
          <ActionsErrorSnackbar />
          <e.Component />
        </>
      )
    })),
  loader,
  action,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
