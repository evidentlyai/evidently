import { decorateAllRoutes, decorateTopLevelRoutes } from 'evidently-ui-lib/router-utils/utils'
import { createBrowserRouter } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import { routes } from '~/routes/routes'

const finalRoutes = routes.map((r) => decorateTopLevelRoutes(r)).map((r) => decorateAllRoutes(r))

export const router = createBrowserRouter(finalRoutes)
