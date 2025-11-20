import type { ButtonProps } from 'evidently-ui-lib/shared-dependencies/mui-material'
import type { HTMLAttributeAnchorTarget } from 'react'
import { RouterLink } from '~/routes/type-safe-route-helpers/components'

type LinkToTraceProps = {
  exportId: string
  projectId: string
  traceId: string
  title?: string
  variant?: ButtonProps['variant']
  target?: HTMLAttributeAnchorTarget | undefined
  startIcon?: React.ReactNode
  endIcon?: React.ReactNode
}

export const LinkToTrace = (props: LinkToTraceProps) => {
  const {
    title = 'Go to trace',
    exportId,
    traceId,
    projectId,
    variant,
    target,
    startIcon,
    endIcon
  } = props

  return (
    <RouterLink
      type='button'
      size='small'
      startIcon={startIcon}
      endIcon={endIcon}
      title={title}
      target={target}
      variant={variant}
      to={'/projects/:projectId/traces/:exportId/trace'}
      paramsToReplace={{ exportId, projectId }}
      query={{ 'trace-id': traceId }}
    />
  )
}
