import { expectJsonRequest } from '~/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from '~/router-utils/components/Error'
import type { ActionSpecialArgs, LoaderSpecialArgs, RouteExtended } from '~/router-utils/types'
import type { LazyRouteFunction, RouteObject } from '~/shared-dependencies/react-router-dom'

import {
  Button,
  type ButtonProps,
  Link,
  Tab,
  type TabProps,
  Typography,
  type TypographyProps
} from '@mui/material'
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
            return r.actionSpecial({ ...args, data } satisfies ActionSpecialArgs)
          }

          return null
        }
      : undefined,
    loader: r.loaderSpecial
      ? async (args) => {
          const { searchParams } = new URL(args.request.url)
          const query = Object.fromEntries(searchParams)

          if (r.loaderSpecial) {
            return r.loaderSpecial({ ...args, searchParams, query } satisfies LoaderSpecialArgs)
          }

          return null
        }
      : undefined
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

export type RouterLinkTemplateComponentProps =
  | ({
      type: 'button'
    } & RLB)
  | ({
      type: 'link'
    } & RLL)
  | ({
      type: 'tab'
    } & RLT)

export const RouterLinkTemplate = (props: RouterLinkTemplateComponentProps) => {
  return props.type === 'button' ? (
    <RLBComponent {...props} />
  ) : props.type === 'tab' ? (
    <RLTComponent {...props} />
  ) : (
    <RLLComponent {...props} />
  )
}

export type RLB = {
  to: string
  title?: string
} & ButtonProps

export const RLBComponent = ({ to, title, ...buttonProps }: RLB) => {
  return (
    <Button component={ReactRouterLink} to={to} {...buttonProps}>
      {title}
    </Button>
  )
}

export type RLL = {
  children?: React.ReactNode
  to: string
  title?: string
} & TypographyProps

export const RLLComponent = ({ children, to, title, ...typographyProps }: RLL) => {
  return (
    <Link component={ReactRouterLink} to={to}>
      <>
        {title && <Typography {...typographyProps}>{title}</Typography>}
        {children}
      </>
    </Link>
  )
}

export type RLT = {
  to: string
} & TabProps

export const RLTComponent = ({ to, ...tabProps }: RLT) => {
  return <Tab component={ReactRouterLink} to={to} {...tabProps} />
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