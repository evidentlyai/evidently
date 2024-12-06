import {
  RouterLinkTemplate,
  type RouterLinkTemplateComponentProps
} from 'evidently-ui-lib/router-utils/components/link'

import type { GetParams } from 'evidently-ui-lib/router-utils/types'
import { useMatch } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import type { GetRouteByPath, Routes } from './types'

import { replaceParamsInLink } from 'evidently-ui-lib/router-utils/utils'

type Paths = Routes['path']

type RouterLinkProps<K extends Paths> = RouterLinkTemplateComponentProps & {
  to: K
  paramsToReplace: GetParams<K>
  query?: GetRouteByPath<K>['loader']['query']
}

export const RouterLink = <K extends Paths>({
  query,
  to,
  paramsToReplace,
  ...props
}: RouterLinkProps<K>) => {
  const searchParams =
    query &&
    new URLSearchParams(
      Object.fromEntries(Object.entries(query).filter(([_, v]) => v)) as Record<string, string>
    )

  const toActual = [replaceParamsInLink(paramsToReplace, to), searchParams].join('?')

  return <RouterLinkTemplate {...props} to={toActual} />
}

export const useMatchRouter = <K extends Paths>({ path }: { path: K }) => {
  return Boolean(useMatch({ path, end: false }))
}
