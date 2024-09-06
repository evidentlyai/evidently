import { Box, Breadcrumbs, Link } from '@mui/material'
import { Link as RouterLink, useMatches } from 'react-router-dom'

interface Crumb {
  to: string
  linkText: string
}

type MatchObject = ReturnType<typeof useMatches>[number]

export type crumbFunction<T> = (
  data: T,
  options: Pick<MatchObject, 'id' | 'params' | 'pathname'>
) => Crumb

type MatchWithCrumbHandle = MatchObject & {
  handle: {
    // biome-ignore lint: <explanation>
    crumb: crumbFunction<any>
  }
}

const isCrumb = (match: MatchObject): match is MatchWithCrumbHandle =>
  // fine for now
  typeof (match as MatchWithCrumbHandle)?.handle?.crumb === 'function'

export const BreadCrumbs = () => {
  const matches = useMatches()
  const crumbs = matches
    .filter(isCrumb)
    .map(({ handle, data, id, pathname, params }) => handle.crumb(data, { id, pathname, params }))

  return (
    <Box>
      <Breadcrumbs aria-label='breadcrumb'>
        {crumbs.map((crumb) => (
          <Link key={crumb.to} component={RouterLink} color='inherit' to={crumb.to}>
            {crumb.linkText}
          </Link>
        ))}
      </Breadcrumbs>
    </Box>
  )
}
