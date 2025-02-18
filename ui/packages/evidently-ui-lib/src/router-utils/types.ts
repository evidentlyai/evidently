import type { ActionFunctionArgs, LoaderFunctionArgs, RouteObject } from 'react-router-dom'

// biome-ignore lint/suspicious/noExplicitAny: fine
export type AdditionalActionFunctionArg = { data: any }

export type ActionArgs<T extends AdditionalActionFunctionArg = AdditionalActionFunctionArg> =
  ActionFunctionArgs & T

export type AdditionalLoaderFunctionArgs = { queryKeys: string }

type QueryKeysToObject<T extends AdditionalLoaderFunctionArgs | undefined> = T extends {
  queryKeys: string
}
  ? Partial<Record<T['queryKeys'], string>>
  : // biome-ignore lint/complexity/noBannedTypes: fine
    {}

export type loadDataArgs<T extends AdditionalLoaderFunctionArgs = AdditionalLoaderFunctionArgs> =
  LoaderFunctionArgs & { searchParams: URLSearchParams } & {
    query: QueryKeysToObject<T>
  }

export type RouteExtended = RouteObject & {
  // biome-ignore lint/suspicious/noExplicitAny: fine
  actions?: Record<string, (args: ActionArgs) => any>
} & {
  // biome-ignore lint/suspicious/noExplicitAny: fine
  loadData?: (args: loadDataArgs) => any
} & { currentRoutePath?: string }

type ExtractPath<T extends RouteExtended> = T['path'] extends string ? T['path'] : ''

export type ProvideLoaderInfo<K, Z> = { query: K; returnType: Z }
export type ProvideActionInfo<K, Z> = { requestData: K; returnType: Z }

type ExtractLoader<T extends RouteExtended> = T['loadData'] extends (
  args: loadDataArgs<infer Z>
) => Promise<infer U>
  ? ProvideLoaderInfo<QueryKeysToObject<Z>, U>
  : // biome-ignore lint/suspicious/noExplicitAny: <explanation>
    T['lazy'] extends (args: any) => Promise<infer R>
    ? R extends RouteExtended
      ? ExtractLoader<R>
      : undefined
    : undefined

type ExtractAction<T extends RouteExtended> = T['actions'] extends Record<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: <explanation>
  (args: ActionArgs) => any
>
  ? {
      [K in keyof T['actions']]: T['actions'][K] extends (
        args: ActionArgs<infer Z>
      ) => Promise<infer O>
        ? ProvideActionInfo<Z['data'], O>
        : undefined
    }
  : // biome-ignore lint/suspicious/noExplicitAny: <explanation>
    T['lazy'] extends (args: any) => Promise<infer R>
    ? R extends RouteExtended
      ? ExtractAction<R>
      : undefined
    : undefined

type IsIndex<T extends RouteExtended> = T['index'] extends true
  ? true
  : T['lazy'] extends (
        // biome-ignore lint/suspicious/noExplicitAny: fine
        args: any
      ) => Promise<{ index: infer Z }>
    ? Z
    : false

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

export type GetRouteStructure<
  T extends readonly RouteExtended[] | undefined,
  Prefix extends string = ''
> = T extends readonly [infer First extends RouteExtended, ...infer Rest extends RouteExtended[]]
  ?
      | {
          expected: `${Prefix}${PathDelimitter<Prefix>}${IsIndex<First> extends true ? '?index' : ''}${ExtractPath<First>}`
          actuall: First['currentRoutePath'] extends string
            ? First['currentRoutePath']
            : First['lazy'] extends (
                  // biome-ignore lint/suspicious/noExplicitAny: fine
                  args: any
                ) => Promise<{ currentRoutePath: infer Z }>
              ? Z
              : 'missing export currentRoutePath in expected route'
        }
      | GetRouteStructure<
          First['children'],
          `${Prefix}${PathDelimitter<Prefix>}${ExtractPath<First>}`
        >
      | GetRouteStructure<Rest, Prefix>
  : never

export type ExpectEqActuall<T> = T extends { expected: infer E; actuall: infer A }
  ? E extends A
    ? true
    : { Error: T }
  : false

type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
  ? Param | ExtractParams<`/${Rest}`>
  : T extends `${string}:${infer Param}`
    ? Param
    : never

export type Match<Path extends string, L, A> = {
  path: Path
  loader: L
  action: A
  params: { [Z in ExtractParams<Path>]: string }
}

export type MatchAny = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  ProvideLoaderInfo<Partial<Record<string, string>>, any> | undefined,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  Record<string, ProvideActionInfo<any, any>> | undefined
>

export type MatchWithAction = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  any, // any loader
  // biome-ignore lint/suspicious/noExplicitAny: fine
  Record<string, ProvideActionInfo<any, any>>
>

export type MatchWithLoader = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  ProvideLoaderInfo<Partial<Record<string, string>>, any>,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  any // any action
>

export type GetParams<K extends string> = { [Z in ExtractParams<K>]: string }

type ExtractMatch<K extends string, M> = Extract<M, { path: K }>

type ExtractQuery<K extends string, M> = ExtractMatch<K, M> extends MatchWithLoader
  ? ExtractMatch<K, M>['loader']['query']
  : undefined

export type GetLinkParams<K extends string, Matches> = keyof GetParams<K> extends never
  ? {
      to: K
      query?: ExtractQuery<K, Matches>
      // biome-ignore lint/complexity/noBannedTypes: fine
      paramsToReplace?: {}
    }
  : {
      to: K
      query?: ExtractQuery<K, Matches>
      paramsToReplace: GetParams<K>
    }

export type GetLinkParamsByPathOnly<K extends string> = keyof GetParams<K> extends never
  ? {
      to: K
      // biome-ignore lint/complexity/noBannedTypes: fine
      paramsToReplace?: {}
    }
  : {
      to: K
      paramsToReplace: GetParams<K>
    }

export type GetParamsOptional<K extends string> = keyof GetParams<K> extends never
  ? // biome-ignore lint/complexity/noBannedTypes: fine
    { paramsToReplace?: {} }
  : { paramsToReplace: GetParams<K> }
