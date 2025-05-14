import {
  Button,
  type ButtonProps,
  IconButton,
  type IconButtonProps,
  Link,
  Tab,
  type TabProps,
  Typography,
  type TypographyProps
} from '@mui/material'
import type { HTMLAttributeAnchorTarget } from 'react'
import {
  type LinkProps,
  Navigate,
  type NavigateProps,
  Link as ReactRouterLink
} from 'react-router-dom'
import { makeRouteUrl } from 'router-utils/router-builder'
import type { GetLinkParams, MatchAny } from 'router-utils/types'
import { assertNever } from '~/utils'

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
  | ({
      type: 'icon'
    } & RLI)

const RouterLinkTemplate = (props: RouterLinkTemplateComponentProps) => {
  const type = props.type
  return type === 'button' ? (
    <RLBComponent {...props} />
  ) : type === 'tab' ? (
    <RLTComponent {...props} />
  ) : type === 'link' ? (
    <RLLComponent {...props} />
  ) : type === 'icon' ? (
    <RLIComponent {...props} />
  ) : (
    assertNever(type)
  )
}

type CommonLinkProps = Omit<LinkProps, 'to' | 'relative'>

type RLB = CommonLinkProps & {
  to: string
  title?: string
  target?: HTMLAttributeAnchorTarget | undefined
} & ButtonProps

const RLBComponent = ({ to, title, target, ...buttonProps }: RLB) => {
  return (
    <Button component={ReactRouterLink} to={to} target={target} {...buttonProps}>
      {title}
    </Button>
  )
}

type RLL = {
  children?: React.ReactNode
  to: string
  title?: string
  linkProps?: CommonLinkProps
} & TypographyProps

const RLLComponent = ({ children, to, title, linkProps, ...typographyProps }: RLL) => {
  return (
    <Link component={ReactRouterLink} to={to} sx={typographyProps.sx} {...linkProps}>
      <>
        {title && <Typography {...typographyProps}>{title}</Typography>}
        {children}
      </>
    </Link>
  )
}

type RLT = CommonLinkProps & {
  to: string
} & TabProps

const RLTComponent = ({ to, ...tabProps }: RLT) => {
  return <Tab component={ReactRouterLink} to={to} {...tabProps} />
}

type RLI = { to: string; IconButtonProps?: CommonLinkProps & IconButtonProps }

const RLIComponent = ({ to, IconButtonProps }: RLI) => {
  return <IconButton component={ReactRouterLink} to={to} {...IconButtonProps} />
}

export const CreateRouterLinkComponent = <M extends MatchAny>() => {
  const Component = <K extends M['path']>({
    to,
    paramsToReplace = {},
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
    query,
    paramsToReplace = {},
    ...props
  }: GetLinkParams<K, M> & Omit<NavigateProps, 'to'>) => {
    const toActual = makeRouteUrl({ paramsToReplace, query, path: to })

    return <Navigate to={toActual} {...props} />
  }

  return Component
}
