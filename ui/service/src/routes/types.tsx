import type { GetMatches } from 'evidently-ui-lib/router-utils/types'
import type { routes } from '~/routes/router'

export type Routes = GetMatches<typeof routes>

export type GetRouteByPath<K extends Routes['path']> = Extract<Routes, { path: K }>
