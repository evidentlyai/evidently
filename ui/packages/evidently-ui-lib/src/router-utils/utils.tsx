import { expectJsonRequest } from '~/api/utils'
import { GenericErrorBoundary, handleActionFetchersErrors } from '~/router-utils/components/Error'
import type { ActionSpecialArgs, LoaderSpecialArgs, RouteExtended } from '~/router-utils/types'
import type {
  ActionFunction,
  LazyRouteFunction,
  LoaderFunction,
  RouteObject
} from '~/shared-dependencies/react-router-dom'

import {
  Button,
  type ButtonProps,
  Link,
  Tab,
  type TabProps,
  Typography,
  type TypographyProps
} from '@mui/material'
import { Outlet, Link as ReactRouterLink } from 'react-router-dom'

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
      action: r.actionSpecial ? replaceActionSpecial(r.actionSpecial) : undefined,
      loader: r.loaderSpecial ? replaceLoaderSpecial(r.loaderSpecial) : undefined,
      ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : ErrorBoundary,
      children: r.children ? r.children.map((r) => decorateAllRoutes(r, ErrorBoundary)) : undefined
    }
  }

  return {
    ...r,
    children: r.children ? r.children.map((r) => decorateAllRoutes(r, ErrorBoundary)) : undefined,
    ErrorBoundary: r.ErrorBoundary ? r.ErrorBoundary : ErrorBoundary,
    action: r.actionSpecial ? replaceActionSpecial(r.actionSpecial) : undefined,
    loader: r.loaderSpecial ? replaceLoaderSpecial(r.loaderSpecial) : undefined
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

export function PrefixRoute<K extends string>({
  prefix,
  crumbTitle
}: { prefix: K; crumbTitle: string }) {
  return {
    path: prefix,
    Component: () => <Outlet />,
    handle: {
      crumb: { title: crumbTitle } satisfies CrumbDefinition
    }
  }
}
