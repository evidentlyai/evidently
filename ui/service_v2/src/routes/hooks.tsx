import {
  createUseLoaderGeneral,
  createUseSubmitFetcherGeneral
} from 'evidently-ui-lib/router-utils/fetchers'
import { createUseMatchRouter } from 'evidently-ui-lib/router-utils/hooks'
import type { Routes } from 'routes/types'

export const useSubmitFetcher = createUseSubmitFetcherGeneral<Routes>()
export const useLoader = createUseLoaderGeneral<Routes>()
export const useMatchRouter = createUseMatchRouter<Routes>()
