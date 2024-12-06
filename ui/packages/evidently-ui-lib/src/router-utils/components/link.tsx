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
