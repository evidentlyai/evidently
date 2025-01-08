import {
  Button,
  type ButtonProps,
  Link,
  Tab,
  type TabProps,
  Typography,
  type TypographyProps
} from '@mui/material'
import { Navigate, type NavigateProps, Link as ReactRouterLink } from 'react-router-dom'
import type { GetParams, MatchAny, MatchWithLoader } from 'router-utils/types'
import { makeRouteUrl } from 'router-utils/utils'

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

const RouterLinkTemplate = (props: RouterLinkTemplateComponentProps) => {
  return props.type === 'button' ? (
    <RLBComponent {...props} />
  ) : props.type === 'tab' ? (
    <RLTComponent {...props} />
  ) : (
    <RLLComponent {...props} />
  )
}

type RLB = {
  to: string
  title?: string
} & ButtonProps

const RLBComponent = ({ to, title, ...buttonProps }: RLB) => {
  return (
    <Button component={ReactRouterLink} to={to} {...buttonProps}>
      {title}
    </Button>
  )
}

type RLL = {
  children?: React.ReactNode
  to: string
  title?: string
} & TypographyProps

const RLLComponent = ({ children, to, title, ...typographyProps }: RLL) => {
  return (
    <Link component={ReactRouterLink} to={to} sx={typographyProps.sx}>
      <>
        {title && <Typography {...typographyProps}>{title}</Typography>}
        {children}
      </>
    </Link>
  )
}

type RLT = {
  to: string
} & TabProps

const RLTComponent = ({ to, ...tabProps }: RLT) => {
  return <Tab component={ReactRouterLink} to={to} {...tabProps} />
}

type ExtractMatch<K extends string, M> = Extract<M, { path: K }>

type GetLinkParams<K extends string, Matches> = {
  to: K
  paramsToReplace: GetParams<K>
  query?: ExtractMatch<K, Matches> extends MatchWithLoader
    ? ExtractMatch<K, Matches>['loader']['query']
    : undefined
}

export const CreateRouterLinkComponent = <M extends MatchAny>() => {
  const Component = <K extends M['path']>({
    to,
    paramsToReplace,
    query,
    ...props
  }: GetLinkParams<K, M> & RouterLinkTemplateComponentProps) => {
    const toActual = makeRouteUrl({ paramsToReplace, query, path: to })

    return <RouterLinkTemplate {...props} to={toActual} />
  }

  return Component
}

export const CreateRouterNavigate = <M extends MatchAny>() => {
  const Component = <K extends M['path']>({
    to,
    paramsToReplace,
    query,
    ...props
  }: GetLinkParams<K, M> & Omit<NavigateProps, 'to'>) => {
    const toActual = makeRouteUrl({ paramsToReplace, query, path: to })

    return <Navigate to={toActual} {...props} />
  }

  return Component
}
