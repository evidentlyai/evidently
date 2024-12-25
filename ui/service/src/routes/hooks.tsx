import { createUseSubmitFetcherGeneral } from 'evidently-ui-lib/router-utils/fetchers'
import type { Routes } from 'routes/types'

export const useSubmitFetcher = createUseSubmitFetcherGeneral<Routes>()
