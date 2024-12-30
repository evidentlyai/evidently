import {
  createUseLoaderGeneral,
  createUseSubmitFetcherGeneral,
  createUseSubmitGeneral
} from 'evidently-ui-lib/router-utils/fetchers'
import type { Routes } from 'routes/types'

export const useSubmitFetcher = createUseSubmitFetcherGeneral<Routes>()
export const useSubmitNavigation = createUseSubmitGeneral<Routes>()
export const useLoader = createUseLoaderGeneral<Routes>()
