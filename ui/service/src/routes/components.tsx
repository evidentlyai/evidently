import {
  RouterLinkTemplate,
  type RouterLinkTemplateComponentProps,
  replaceParamsInLink
} from 'evidently-ui-lib/router-utils/utils'

import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import { useMatch } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import type { GetRouteByPath, Routes } from './types'

type Paths = Routes['path']

type RouterLinkProps<K extends Paths> = RouterLinkTemplateComponentProps & {
  to: K
  paramsToReplace: GetParams<K>
  query?: GetRouteByPath<K>['loader']['query']
}

export const RouterLink = <K extends Paths>({ ...props }: RouterLinkProps<K>) => {
  const searchParams =
    props.query &&
    new URLSearchParams(
      Object.fromEntries(Object.entries(props.query).filter(([_, v]) => v)) as Record<
        string,
        string
      >
    )

  const to = [replaceParamsInLink(props.paramsToReplace, props.to), searchParams].join('?')

  return <RouterLinkTemplate {...props} to={to} />
}

export const useMatchRouter = <K extends Paths>({ path }: { path: K }) => {
  return Boolean(useMatch({ path, end: false }))
}
