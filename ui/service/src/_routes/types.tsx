import type { GetMatches, ReplaceAllDynamicSegments } from 'evidently-ui-lib/router-utils/types'
import type { routes } from '~/_routes/router'

export type Routes = GetMatches<typeof routes>

export type GetRouteByPath<K extends Routes['path']> = Extract<Routes, { path: K }>

export type PathsWithDynamicSegments = ReplaceAllDynamicSegments<Routes['path']>
