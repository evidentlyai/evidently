import type { Expect } from 'evidently-ui-lib/api/types/utils'

import type {
  ExpectEqActuall,
  GetMatches,
  GetRouteStructure,
  MatchWithLoader
} from 'evidently-ui-lib/router-utils/types'

import type { routes } from 'routes/src'

export type Routes = GetMatches<typeof routes>

export type Paths = Routes['path']

type RoutesWithLoader = Extract<Routes, MatchWithLoader>

type PathsRoutesWithLoader = RoutesWithLoader['path']
export type GetRouteByPath<K extends PathsRoutesWithLoader> = Extract<RoutesWithLoader, { path: K }>

export type __TESTS_ROUTE_STRUCTURE = Expect<ExpectEqActuall<GetRouteStructure<typeof routes>>>
