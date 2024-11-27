import { expectJsonRequest } from '~/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from '~/components/Error'
import type { RouteExtended } from '~/router-utils/types'
import type { LazyRouteFunction, RouteObject } from '~/shared-dependencies/react-router-dom'

import { Link, Typography, type TypographyProps } from '@mui/material'
import { Link as ReactRouterLink } from 'react-router-dom'

export type CrumbDefinition = { title?: string; param?: string; keyFromLoaderData?: string }

export type HandleWithCrumb = { crumb?: CrumbDefinition }

export const decorateAllRoutes = (r: RouteExtended): RouteExtended => {
  if (r.lazy) {
    // @ts-ignore
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decorateAllRoutes)) as LazyRouteFunction<RouteObject>,
      children: r.children ? r.children.map(decorateAllRoutes) : undefined
    }
  }

  return {
    ...r,
    children: r.children ? r.children.map(decorateAllRoutes) : undefined,
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

export const decarateTopLevelRoutes = (r: RouteExtended): RouteExtended => {
  if (r.lazy) {
    return {
      ...r,
      lazy: (() => r.lazy?.().then(decarateTopLevelRoutes)) as LazyRouteFunction<RouteObject>
    }
  }

  if (r.Component) {
    return { ...r, ...handleActionFetchersErrors({ Component: r.Component }) }
  }

  return r
}

export type RouterLinkTemplateComponentProps = {
  children?: React.ReactNode
  to: string
  title?: string
  typographyProps?: TypographyProps
}

export const RouterLinkTemplateComponent = ({
  children,
  to,
  title,
  typographyProps
}: RouterLinkTemplateComponentProps) => {
  return (
    <Link component={ReactRouterLink} to={to}>
      <>
        {title && <Typography {...typographyProps}>{title}</Typography>}
        {children}
      </>
    </Link>
  )
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
