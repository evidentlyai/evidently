import {
  RouterLinkTemplateComponent,
  type RouterLinkTemplateComponentProps,
  replaceParamsInLink
} from 'evidently-ui-lib/router-utils/utils'

import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import type { Routes } from './types'

type RouterLinkProps<K extends string> = RouterLinkTemplateComponentProps & {
  to: K
  paramsToReplace: GetParams<K>
}

export const RouterLink = <K extends Routes['path']>({ ...props }: RouterLinkProps<K>) => (
  <RouterLinkTemplateComponent
    {...props}
    to={replaceParamsInLink(props.paramsToReplace, props.to)}
  />
)
