import type { ActionFunctionArgs, RouteObject } from 'react-router-dom'

// biome-ignore lint/suspicious/noExplicitAny: fine
export type AdditionalActionFunctionArg = { data: any }

export type ActionSpecialArgs<T extends AdditionalActionFunctionArg = AdditionalActionFunctionArg> =
  ActionFunctionArgs & T

// biome-ignore lint/suspicious/noExplicitAny: fine
export type RouteExtended = RouteObject & { actionSpecial?: (args: ActionSpecialArgs) => any }

type ExtractPath<T extends RouteExtended> = T['path'] extends string ? T['path'] : ''

export type ProvideLoaderInfo<K> = { returnType: K }
export type ProvideActionInfo<K, Z> = { requestData: K; returnType: Z }

// biome-ignore lint/suspicious/noExplicitAny: fine
type ExtractLoader<T extends RouteExtended> = T['loader'] extends (args: any) => Promise<infer U>
  ? ProvideLoaderInfo<U>
  : // biome-ignore lint/suspicious/noExplicitAny: fine
    T['lazy'] extends (args: any) => Promise<{ loader: (args: any) => Promise<infer K> }>
    ? ProvideLoaderInfo<K>
    : undefined

type ExtractAction<T extends RouteExtended> = T['actionSpecial'] extends (
  args: ActionSpecialArgs<infer Z>
) => Promise<infer O>
  ? ProvideActionInfo<Z['data'], O>
  : T['lazy'] extends (
        // biome-ignore lint/suspicious/noExplicitAny: fine
        args: any
      ) => Promise<{ actionSpecial: (args: ActionSpecialArgs<infer Z>) => Promise<infer O> }>
    ? ProvideActionInfo<Z['data'], O>
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
  params: { [Z in ExtractParams<Path>]: string }
}

export type MatchWithAction = Match<
  string,
  // biome-ignore lint/suspicious/noExplicitAny: fine
  any, // any loader
  // biome-ignore lint/suspicious/noExplicitAny: fine
  ProvideActionInfo<any, any>
>

export type GetParams<K extends string> = { [Z in ExtractParams<K>]: string }
