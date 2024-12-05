import {
  RouterLinkTemplate,
  type RouterLinkTemplateComponentProps,
  replaceParamsInLink
} from 'evidently-ui-lib/router-utils/utils'

import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import { useMatch } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import type { Routes } from './types'

type RouterLinkProps<K extends string> = RouterLinkTemplateComponentProps & {
  to: K
  paramsToReplace: GetParams<K>
}

type Paths = Routes['path']

export const RouterLink = <K extends Paths>({ ...props }: RouterLinkProps<K>) => (
  <RouterLinkTemplate {...props} to={replaceParamsInLink(props.paramsToReplace, props.to)} />
)

export const useMatchRouter = <K extends Paths>({ path }: { path: K }) => {
  return Boolean(useMatch({ path, end: false }))
}
