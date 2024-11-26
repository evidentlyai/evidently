import {
  RouterLinkTemplateComponent,
  type RouterLinkTemplateComponentProps,
  replaceParamsInLink
} from 'evidently-ui-lib/router-utils/utils'

import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import type { Routes } from './types'

type RouterLinkProps<K extends string> = Omit<RouterLinkTemplateComponentProps, 'to'> & {
  to: K
  paramsToReplace: GetParams<K>
}

export const RouterLink = <K extends Routes['path']>({
  children,
  to,
  paramsToReplace,
  ...props
}: RouterLinkProps<K>) => (
  <RouterLinkTemplateComponent to={replaceParamsInLink(paramsToReplace, to)} {...props}>
    {children}
  </RouterLinkTemplateComponent>
)
