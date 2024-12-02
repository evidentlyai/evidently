import { Box, Breadcrumbs as BreadcrumbsMaterial, Link } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'

interface Crumb {
  to: string
  linkText: string
}

export const BreadCrumbs = ({ crumbs }: { crumbs: Crumb[] }) => {
  return (
    <Box>
      <BreadcrumbsMaterial aria-label='breadcrumb'>
        {crumbs.map((crumb) => (
          <Link key={crumb.to} component={RouterLink} color='inherit' to={crumb.to}>
            {crumb.linkText}
          </Link>
        ))}
      </BreadcrumbsMaterial>
    </Box>
  )
}
