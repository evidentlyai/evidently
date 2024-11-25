import type { routes } from '~/_routes/router'

import type {
  ActionFunctionArgs,
  RouteObject
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'

// biome-ignore lint/suspicious/noExplicitAny: fine
export type ActionSpecialArgs<T extends { data: object } = { data: any }> = ActionFunctionArgs & T

// biome-ignore lint/suspicious/noExplicitAny: fine
export type RouteExtended = RouteObject & { actionSpecial?: (args: ActionSpecialArgs) => any }

type ExtractPath<T extends RouteExtended> = T['path'] extends string ? T['path'] : ''

// biome-ignore lint/suspicious/noExplicitAny: fine
type ExtractLoader<T extends RouteExtended> = T['loader'] extends (args: any) => Promise<infer U>
  ? { returnType: U }
  : undefined

type ExtractAction<T extends RouteExtended> = T['actionSpecial'] extends (
  args: ActionSpecialArgs<infer Z>
) => Promise<infer O>
  ? { args: Z; returnType: O }
  : undefined

type IsIndex<T extends RouteExtended> = T['index'] extends true ? true : false

type PathDelimitter<T extends string> = T extends `${string}/` ? '' : '/'

export type GetMatches<
  T extends readonly RouteExtended[] | undefined,
  Prefix extends string = ''
> = T extends readonly [infer First extends RouteExtended, ...infer Rest extends RouteExtended[]]
  ?
      | Match<
          `${Prefix}${PathDelimitter<Prefix>}${IsIndex<First> extends true ? '?index' : ''}${ExtractPath<First>}`,
          ExtractLoader<First>,
          ExtractAction<First>
        >
      | GetMatches<First['children'], `${Prefix}${PathDelimitter<Prefix>}${ExtractPath<First>}`>
      | GetMatches<Rest, Prefix>
  : never

type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
  ? Param | ExtractParams<`/${Rest}`>
  : T extends `${string}:${infer Param}`
    ? Param
    : never

export type Match<Path extends string, L, A> = {
  path: Path
  loader: L
  action: A
  params: Record<ExtractParams<Path>, string>
}

export type Routes = GetMatches<typeof routes>

export type GetRouteByPath<K extends Routes['path']> = Extract<Routes, { path: K }>

export type ReplaceAllDynamicSegments<
  T extends string,
  K extends string = string
> = T extends `${infer Start}/:${string}/${infer Rest}`
  ? `${Start}/${K}/${ReplaceAllDynamicSegments<`${Rest}`, K>}`
  : T extends `${infer Start}/:${string}`
    ? `${Start}/${K}`
    : T

export type PathsWithDynamicSegments = ReplaceAllDynamicSegments<Routes['path']>

export const isPathMatchesRoutes: <T extends string>(
  arg: Extract<PathsWithDynamicSegments, T>
) => T = (a) => a
