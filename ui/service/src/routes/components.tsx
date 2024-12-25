import { CreateRouterLinkComponent } from 'evidently-ui-lib/router-utils/components/link'
import { createUseMatchRouter } from 'evidently-ui-lib/router-utils/hooks'
import type { Routes } from 'routes/types'

export const RouterLink = CreateRouterLinkComponent<Routes>()

export const useMatchRouter = createUseMatchRouter<Routes>()
