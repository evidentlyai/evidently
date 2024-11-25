import { expectJsonRequest } from 'evidently-ui-lib/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from 'evidently-ui-lib/components/Error'
import type {
  LazyRouteFunction,
  RouteObject
} from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import type { PathsWithDynamicSegments, RouteExtended } from '~/_routes/types'

export type CrumbDefinition = { title?: string; param?: string; keyFromLoaderData?: string }

export type HandleWithCrumb = { crumb?: CrumbDefinition }

export const decorateAllRoute = (r: RouteExtended): RouteExtended => {
  if (r.lazy) {
    // @ts-ignore
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decorateAllRoute)) as LazyRouteFunction<RouteObject>,
      children: r.children ? r.children.map(decorateAllRoute) : undefined
    }
  }

  return {
    ...r,
    children: r.children ? r.children.map(decorateAllRoute) : undefined,
    ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : GenericErrorBoundary,
    action: r.actionSpecial
      ? async (args) => {
          expectJsonRequest(args.request)

          const data = await args.request.json()

          if (r.actionSpecial) {
            return r.actionSpecial({ ...args, data })
          }

          return null
        }
      : undefined
  } as RouteExtended
}

export const decarateTopLevelRoute = (r: RouteExtended): RouteExtended => {
  if (r.lazy) {
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decarateTopLevelRoute)) as LazyRouteFunction<RouteObject>
    }
  }

  if (r.Component) {
    return { ...r, ...handleActionFetchersErrors({ Component: r.Component }) }
  }

  return r
}

export const isPathMatchesRoutes: <T extends string>(
  arg: Extract<PathsWithDynamicSegments, T>
) => T = (a) => a
