import { expectJsonRequest } from '~/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from '~/router-utils/components/Error'
import type { ActionSpecialArgs, LoaderSpecialArgs, RouteExtended } from '~/router-utils/types'
import type {
  ActionFunction,
  LazyRouteFunction,
  LoaderFunction,
  RouteObject
} from '~/shared-dependencies/react-router-dom'

export type CrumbDefinition = { title?: string; param?: string; keyFromLoaderData?: string }

export type HandleWithCrumb = { crumb?: CrumbDefinition }

// biome-ignore lint/suspicious/noExplicitAny: fine
const replaceLoaderSpecial = (loaderSpecial: (args: LoaderSpecialArgs) => any) => {
  const loader: LoaderFunction = async (args) => {
    const { searchParams } = new URL(args.request.url)
    const query = Object.fromEntries(searchParams)

    return loaderSpecial({ ...args, searchParams, query })
  }

  return loader
}

// biome-ignore lint/suspicious/noExplicitAny: fine
const replaceActionSpecial = (actionSpecial: (args: ActionSpecialArgs) => any) => {
  const action: ActionFunction = async (args) => {
    expectJsonRequest(args.request)
    const data = await args.request.json()

    return actionSpecial({ ...args, data })
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
      loader: r.loaderSpecial ? replaceLoaderSpecial(r.loaderSpecial) : undefined,
      action: r.actionSpecial ? replaceActionSpecial(r.actionSpecial) : undefined,
      ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : ErrorBoundary,
      children: r.children ? r.children.map((r) => decorateAllRoutes(r, ErrorBoundary)) : undefined
    }
  }

  return {
    ...r,
    loader: r.loaderSpecial ? replaceLoaderSpecial(r.loaderSpecial) : undefined,
    action: r.actionSpecial ? replaceActionSpecial(r.actionSpecial) : undefined,
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
    return { ...r, ...handleActionFetchersErrors({ Component: r.Component }) }
  }

  return r
}

export const replaceParamsInLink = (paramsToReplace: Record<string, string>, path: string) => {
  const result = path
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

  return result
}

export const provideCrumb = (crumb: CrumbDefinition) => ({ handle: { crumb } })

export const Route: <K extends RouteExtended, A extends RouteExtended>(a: K, b: A) => K & A = (
  a,
  b
) => {
  return { ...a, ...b }
}
