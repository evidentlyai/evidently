import { useMatches } from 'evidently-ui-lib/shared-dependencies/react-router-dom'
import type { HandleWithCrumb } from '~/_routes/utils'

export const useCrumbs = () => {
  const matches = useMatches()

  const crumbs = matches
    .filter((e) => (e.handle as HandleWithCrumb)?.crumb)
    .map(({ handle, data, pathname, params }) => ({
      to: pathname,
      linkText:
        (handle as HandleWithCrumb)?.crumb?.title ??
        params[(handle as HandleWithCrumb)?.crumb?.param ?? ''] ??
        (typeof data === 'object'
          ? (data as Record<string, string>)[
              (handle as HandleWithCrumb)?.crumb?.keyFromLoaderData ?? ''
            ]
          : '') ??
        `undefined (provide title or param in crumb). Path: ${pathname}`
    }))

  return { crumbs }
}
