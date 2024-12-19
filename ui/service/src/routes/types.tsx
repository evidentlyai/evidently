import type { Expect } from 'evidently-ui-lib/api/types/utils'

import type {
  ExpectEqActuall,
  GetMatches,
  GetRouteStructure
} from 'evidently-ui-lib/router-utils/types'

import type { routes } from '~/routes/routes'

export type Routes = GetMatches<typeof routes>

export type GetRouteByPath<K extends Routes['path']> = Extract<Routes, { path: K }>

export type __TESTS_ROUTE_STRUCTURE = Expect<ExpectEqActuall<GetRouteStructure<typeof routes>>>
