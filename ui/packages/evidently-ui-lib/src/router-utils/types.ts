import type { ActionFunctionArgs, LoaderFunctionArgs, RouteObject } from 'react-router-dom'

// biome-ignore lint/suspicious/noExplicitAny: fine
export type AdditionalActionFunctionArg = { data: any }

export type ActionSpecialArgs<T extends AdditionalActionFunctionArg = AdditionalActionFunctionArg> =
  ActionFunctionArgs & T

export type AdditionalLoaderFunctionArgs = { queryKeys: string }

type QueryKeysToObject<T extends AdditionalLoaderFunctionArgs | undefined> = T extends {
  queryKeys: string
}
  ? Partial<Record<T['queryKeys'], string>>
  : // biome-ignore lint/complexity/noBannedTypes: fine
    {}

export type LoaderSpecialArgs<
  T extends AdditionalLoaderFunctionArgs = AdditionalLoaderFunctionArgs
> = LoaderFunctionArgs & { searchParams: URLSearchParams } & {
  query: QueryKeysToObject<T>
}

// biome-ignore lint/suspicious/noExplicitAny: fine
export type RouteExtended = RouteObject & { actionSpecial?: (args: ActionSpecialArgs) => any } & {
  // biome-ignore lint/suspicious/noExplicitAny: fine
  loaderSpecial?: (args: LoaderSpecialArgs) => any
}

type ExtractPath<T extends RouteExtended> = T['path'] extends string ? T['path'] : ''

export type ProvideLoaderInfo<K, Z> = { query: K; returnType: Z }
export type ProvideActionInfo<K, Z> = { requestData: K; returnType: Z }

type ExtractLoader<T extends RouteExtended> = T['loaderSpecial'] extends (
  args: LoaderSpecialArgs<infer Z>
) => Promise<infer U>
  ? ProvideLoaderInfo<QueryKeysToObject<Z>, U>
  : T['lazy'] extends (
        // biome-ignore lint/suspicious/noExplicitAny: fine
        args: any
      ) => Promise<{ loaderSpecial: (args: LoaderSpecialArgs<infer Z>) => Promise<infer K> }>
    ? ProvideLoaderInfo<QueryKeysToObject<Z>, K>
    : ProvideLoaderInfo<QueryKeysToObject<undefined>, undefined>

type ExtractAction<T extends RouteExtended> = T['actionSpecial'] extends (
  args: ActionSpecialArgs<infer Z>
) => Promise<infer O>
  ? ProvideActionInfo<Z['data'], O>
  : T['lazy'] extends (
        // biome-ignore lint/suspicious/noExplicitAny: fine
        args: any
      ) => Promise<{ actionSpecial: (args: ActionSpecialArgs<infer Z>) => Promise<infer O> }>
    ? ProvideActionInfo<Z['data'], O>
    : ProvideActionInfo<undefined, undefined>

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

export type MatchWithAction = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  any, // any loader
  // biome-ignore lint/suspicious/noExplicitAny: fine
  ProvideActionInfo<any, any>
>

export type MatchWithLoader = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  ProvideLoaderInfo<any, any>,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  any // any action
>

export type GetParams<K extends string> = { [Z in ExtractParams<K>]: string }