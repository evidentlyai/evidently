import type { CrumbDefinition } from 'evidently-ui-lib/router-utils/utils'
import { Outlet } from 'evidently-ui-lib/shared-dependencies/react-router-dom'

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
