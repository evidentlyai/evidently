import { GenericErrorBoundary } from 'evidently-ui-lib/components/Error'
import { getLoaderAction } from 'evidently-ui-lib/routes-components/dashboard/data'
import type { RouteObject } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { clientAPI } from '~/api'

const { loader } = getLoaderAction({ api: clientAPI })

export default {
  index: true,
  id: 'dashboard',
  lazy: async () => {
    return {
      Component: () => (
        <p>
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Hic ad dolores molestias maiores
          enim id. Modi tempore natus, expedita eius beatae, nemo nam non culpa repellat architecto
          error fugit nisi?
        </p>
      )
    }
  },
  loader,
  ErrorBoundary: GenericErrorBoundary
} satisfies RouteObject
