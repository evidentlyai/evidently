import { expectJsonRequest } from '~/api/utils'
import { GenericErrorBoundary, handleFetchersActionErrors } from '~/router-utils/components/error'
import type { ActionArgs, RouteExtended, loadDataArgs } from '~/router-utils/types'
import type {
  ActionFunction,
  LazyRouteFunction,
  LoaderFunction,
  RouteObject
} from '~/shared-dependencies/react-router-dom'
import { assertNeverActionVariant } from '~/utils'

export type CrumbDefinition = { title?: string; param?: string; keyFromLoaderData?: string }

export type HandleWithCrumb = { crumb?: CrumbDefinition }

// biome-ignore lint/suspicious/noExplicitAny: fine
const replaceloadData = (loadData: (args: loadDataArgs) => any) => {
  const loader: LoaderFunction = async (args) => {
    const { searchParams } = new URL(args.request.url)
    const query = Object.fromEntries(searchParams)

    return loadData({ ...args, searchParams, query })
  }

  return loader
}

// biome-ignore lint/suspicious/noExplicitAny: fine
const replaceActions = (actions: Record<string, (args: ActionArgs) => any>) => {
  const action: ActionFunction = async (args) => {
    expectJsonRequest(args.request)

    // biome-ignore lint/suspicious/noExplicitAny: fine
    const { action, data } = (await args.request.json()) as { action: string; data: any }

    if (action in actions) {
      return actions[action]({ ...args, data })
    }

    assertNeverActionVariant(action as never)
  }

  return action
}

export const decorateAllRoutes = (
  r: RouteExtended,
  ErrorBoundary: () => JSX.Element = GenericErrorBoundary
): RouteExtended => {
  if (r.lazy) {
    // @ts-ignore
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decorateAllRoutes)) as LazyRouteFunction<RouteObject>,
      loader: r.loadData ? replaceloadData(r.loadData) : undefined,
      action: r.actions ? replaceActions(r.actions) : undefined,
      ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : ErrorBoundary,
      children: r.children ? r.children.map((r) => decorateAllRoutes(r, ErrorBoundary)) : undefined
    }
  }

  return {
    ...r,
    loader: r.loadData ? replaceloadData(r.loadData) : undefined,
    action: r.actions ? replaceActions(r.actions) : undefined,
    ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : ErrorBoundary,
    children: r.children ? r.children.map((r) => decorateAllRoutes(r, ErrorBoundary)) : undefined
  } as RouteExtended
}

export const decorateTopLevelRoutes = (r: RouteExtended): RouteExtended => {
  if (r.lazy) {
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decorateTopLevelRoutes)) as LazyRouteFunction<RouteObject>
    }
  }

  if (r.Component) {
    return { ...r, ...handleFetchersActionErrors({ Component: r.Component }) }
  }

  return r
}

export const makeRouteUrl = ({
  path,
  paramsToReplace,
  query
}: {
  paramsToReplace: Record<string, string>
  path: string
  query?: Record<string, string | undefined>
}) => {
  const pathWithReplacedParams = path
    .split('/')
    .map((part) => {
      if (part.startsWith(':')) {
        const p = part.slice(1)
        if (p in paramsToReplace) {
          return paramsToReplace[p]
        }
      }

      return part
    })
    .join('/')

  const searchParams =
    query &&
    new URLSearchParams(
      Object.fromEntries(Object.entries(query).filter(([_, v]) => Boolean(v))) as Record<
        string,
        string
      >
    )

  const result = [pathWithReplacedParams, searchParams].filter(Boolean).join('?')

  return result
}

export const provideCrumb = (crumb: CrumbDefinition) => ({ handle: { crumb } })

export const Route: <K extends RouteExtended, A extends RouteExtended>(a: K, b: A) => K & A = (
  a,
  b
) => {
  return { ...a, ...b }
}
