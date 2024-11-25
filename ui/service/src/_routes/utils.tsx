import { expectJsonRequest } from 'evidently-ui-lib/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from 'evidently-ui-lib/components/Error'
import type { RouteExtended } from './types'

export type CrumbDefinition = { title?: string; param?: string; keyFromLoaderData?: string }

export type HandleWithCrumb = { crumb?: CrumbDefinition }

export const decorateAllRoute = (r: RouteExtended): RouteExtended =>
  ({
    ...r,
    children: r.children ? r.children.map(decorateAllRoute) : undefined,
    ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : GenericErrorBoundary,
    action: r.actionSpecial
      ? async (args) => {
          console.log('in action')
          expectJsonRequest(args.request)

          const data = await args.request.json()

          if (r.actionSpecial) {
            return r.actionSpecial({ ...args, data })
          }

          return null
        }
      : undefined
  }) as RouteExtended

export const decarateTopLevelRoute = (r: RouteExtended): RouteExtended =>
  r.Component ? { ...r, ...handleActionFetchersErrors({ Component: r.Component }) } : r
